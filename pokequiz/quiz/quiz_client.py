import logging
import random
import boto3
from operator import itemgetter

from pokequiz.quiz import helpers
from pokequiz.database import QuizQuestionTable, InfoTable
from pokequiz import QUIZ_STORAGE_TABLE, QUIZ_CONFIG

logger = logging.getLogger(__name__)


class Quiz(object):
    def __init__(self, quiz_id, team_id):
        boto_session = boto3.Session()

        logger.debug("Initializing quiz")

        self.quiz_question_table = QuizQuestionTable(
            boto_session=boto_session,
            table_name=QUIZ_STORAGE_TABLE,
            quiz_id=f"{quiz_id}-question",
            primary_key="id",
            range_key="range"
        )

        self.info_table = InfoTable(
            boto_session=boto_session,
            table_name=QUIZ_STORAGE_TABLE,
            quiz_id=f"{quiz_id}-teaminfo",
            primary_key="id",
            range_key="range",
            team_id=team_id
        )

        self.config = QUIZ_CONFIG

    def get_random_quiz_question(self):
        """Gets a random quiz question

        Returns:
            A random quiz question
        """
        return self.quiz_question_table.get_random_value()

    def get_bot_token(self):
        """Gets the bot token for the specific team that is running this quiz.
        This token is set when the user installs the application. The bot then
        uses this token to send messages.
        """
        return self.info_table.get_bot_token()

    def set_oauth_information(self, bot_info, team_name, access_token):
        """Sets Oauth Information in the database

        The Oauth information includes the bot_info which contains the bots_id and its access
        token to use when authenticating to the slack channel
        """
        self.info_table.save_oauth_info(bot_info, team_name, access_token)

    def get_leaderboard(self):
        """Gets the leaderboard values from the database

        Returns:
            A dictionary if there is values and if there isn't it will return a specific string
        """
        try:
            leaderboard = self.info_table.get_user_scores()
        except KeyError:
            return self.config["text"]["no_answered_questions"]
        return leaderboard

    def find_quiz_question(self, question_id):
        """Finds the quiz question based on the question id

        Args:
            question_id: The question id

        """
        return self.quiz_question_table.get_value(question_id)

    def update_user_score(self, user_id, is_correct):
        """Updates a user score based on if they get it correct or not

        Args:
            user_id: The users id
            is_correct: If the user got it correct or not

        Returns:

        """
        if is_correct:
            self.info_table.save_correct_answer(user_id, self.config["values"]["answer_values"]["correct"])
        else:
            self.info_table.save_incorrect_answer(user_id, self.config["values"]["answer_values"]["incorrect"])

    def get_user_streak(self, user_id: str) -> int:
        """Gets a user specific streak

        Args:
            user_id: The users id

        Returns:
            A integer of the users streak
        """
        return self.info_table.get_user_streak(user_id)

    def form_suggest_question_slack_attachment(self, question) -> dict:
        """Forms a slack attachment attachment

        Args:
            question (dict)

        Returns:
            A dictionary of the slack attachment
        """

        fields = []
        actions = []
        question_counter = 1
        answers = []

        # We do this because otherwise the correct answer will keep getting appended
        correct_answer = [question.get("correct_answer")]
        answers.extend(question.get("incorrect_answers"))
        answers.extend(correct_answer)

        # Randomize the order
        random.shuffle(answers)

        # Loops through all the incorrect answers and adds them to the slack attachment
        for answer in answers:
            fields.append(helpers.form_question_field(question_counter, answer))
            actions.append(helpers.form_question_action(question_counter, answer))
            question_counter += 1  # Increment question count

        return {
            "fallback": question.get("question"),
            "pretext": question.get("question"),
            "callback_id": question.get("range"),
            "text": "",
            "attachment_type": "default",
            "fields": fields,
            "actions": actions,
            "color": self.config["cosmetic"]["color"]["orange"]
        }

    def form_answered_question_slack_attachment(self, question, correct=True) -> dict:
        """Forms an answered slack attachment

        Args:
            correct: Was it correct
            question: The question itself

        Returns:
            A dictionary of the slack attachment
        """

        # If the user answered question
        if correct:
            attachment_color = self.config["cosmetic"]["color"]["green"]
        else:
            attachment_color = self.config["cosmetic"]["color"]["red"]

        fields = []

        # Loops through all the incorrect answers and adds them to the slack attachment
        for answer in question.incorrect_answers:
            fields.append(helpers.form_answered_question_field(self.config["cosmetic"]["emoji"]["incorrect"], answer))

        fields.append(helpers.form_answered_question_field(self.config["cosmetic"]["emoji"]["correct"], question.get("correct_answer")))

        return {
            "fallback": question.get("question"),
            "pretext": question.get("question"),
            "callback_id": "answer_question",
            "text": "",
            "attachment_type": "default",
            "fields": fields,
            "color": attachment_color
        }

    def update_question_attachment(self, attachment, correct_answer, is_correct):
        """Updates a question attachment to show the correct answers with emojis

        Args:
            attachment: The question attachment
            correct_answer: The correct answer for the attachment
            is_correct: Did the user answer the question correctly

        Returns:
            A slack attachment with emojis of if its correct or not instead of 1. etc
        """
        new_fields = []
        for field in attachment["fields"]:
            field_value = field["value"]
            # Split the message field
            message_field = field_value.split(" ")
            # Join everything except the first one as it will be the *1:*
            answer = " ".join(message_field[1:])
            if answer == correct_answer:
                new_fields.append(helpers.form_answered_question_field(self.config["cosmetic"]["emoji"]["correct"], answer))
            else:
                new_fields.append(helpers.form_answered_question_field(self.config["cosmetic"]["emoji"]["incorrect"], answer))
        # Remove all the buttons
        attachment["actions"] = []
        # Replace the fields with the new ones
        attachment["fields"] = new_fields

        if is_correct:
            attachment["color"] = self.config["cosmetic"]["color"]["green"]
        else:
            attachment["color"] = self.config["cosmetic"]["color"]["red"]
        return attachment

    def form_leaderboard_text(self, leaderboard: dict):
        """Form a leaderboard mapping forms the leaderboard text to send to slack

        Args:
            leaderboard: The leaderboard dictionary should be returned by

        Returns:

        """
        leaderboard_list = []
        # Put the leaderboard values into a list
        for user_id, scores in leaderboard.items():
            leaderboard_list.append({
                "user_id": user_id,
                "user_score": scores["overall_score"]
            })
        # Sort the leaderboard in descending order
        sorted_leaderboard_list = sorted(leaderboard_list, key=itemgetter('user_score'), reverse=True)
        # Put the header for the leaderboard
        leaderboard_string = f"{self.config['text']['leaderboard']['header']}\n"
        # Start the rank counter
        rank_counter = 1
        for user_score in sorted_leaderboard_list:
            leaderboard_string += f"{rank_counter}. <@{user_score['user_id']}> -  {user_score['user_score']} points\n"
            rank_counter += 1
            if rank_counter > self.config["values"]["leaderboard"]["max_users"]:
                break
        return leaderboard_string

    def form_another_question_attachment(self) -> dict:
        """Forms another question slack attachment

        Returns:
            A dictionary of the slack attachment
        """

        # Creates the action buttons for the yes or no play again.
        yes_no_actions = [
            helpers.form_slack_action("Yes", "Yes", "Yes", style=self.config["cosmetic"]["button_styles"]["green"]),
            helpers.form_slack_action("No", "No", "No", style=self.config["cosmetic"]["button_styles"]["red"])
        ]

        return {
            "fallback": self.config["text"]["play_again"],
            "pretext": self.config["text"]["play_again"],
            "callback_id": "play_again",
            "text": "",
            "attachment_type": "default",
            "actions": yes_no_actions,
            "color": self.config["cosmetic"]["color"]["orange"]
        }
