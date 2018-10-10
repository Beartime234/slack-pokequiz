"""
Slack chat-bot Lambda handler.
"""

# Module Imports
import logging
import json
from slackclient import SlackClient
from urllib.parse import parse_qs

# Local imports
from pokequiz import helpers, messaging, SECRETS, QUIZ_ID

# Import the quiz
from pokequiz.quiz import Quiz

logger = logging.getLogger(__name__)


def lambda_handler(api_event, api_context):
    """Handle an incoming HTTP request from a Slack chat-bot.
    """
    logger.info(f"Api Event: {api_event}")

    # Grab relevant information form the api_event
    slack_body_raw = api_event["body"]
    # Interactive responses are in x-url-form-encoded
    slack_body_dict = parse_qs(slack_body_raw)
    request_headers = api_event["headers"]

    # If the stage is production make sure that we are receiving events from slack otherwise we don't care
    if not helpers.verify_request(request_headers, slack_body_raw, SECRETS["SIGNING_SECRET"]):
        return helpers.form_response(400, {"Error": "Bad Request Signature"})

    # This gets the payload from the user interacting with the component
    slack_payload_dict = json.loads(slack_body_dict["payload"][0])

    logger.info(f"Payload: {slack_payload_dict}")
    # Build the slack client. This allows us make slack API calls
    # read up on the python-slack-client here. We get this from
    # AWS secrets manager. https://github.com/slackapi/python-slackclient

    # Get the channel id
    channel_id = slack_payload_dict["channel"]["id"]

    # Get the user id
    user_id = slack_payload_dict["user"]["id"]

    # Get the team id
    team_id = slack_payload_dict["team"]["id"]

    # Get the previous action time stamp
    previous_action_ts = slack_payload_dict["message_ts"]

    # Get callback_id of the action
    callback_id = slack_payload_dict["callback_id"]

    # Create the quiz object
    quiz = Quiz(QUIZ_ID, team_id)

    sc = SlackClient(quiz.get_bot_token())

    # If the user interacted with the play_again action
    if callback_id == "play_again":

        # Get which action the user clicked
        play_again_response = slack_payload_dict["actions"][0]["value"].lower()

        # If the user wants to play again
        if play_again_response == "yes":

            # Get a new question
            question = quiz.get_random_quiz_question()

            # Send the new question
            messaging.update_play_again(
                slack_client=sc,
                channel_id=channel_id,
                question_attachment=quiz.form_suggest_question_slack_attachment(question),
                ts=previous_action_ts
            )
        else:

            # Delete the play again message because they don't want to
            messaging.delete_play_again(
                slack_client=sc,
                channel_id=channel_id,
                ts=previous_action_ts
            )
    else:  # This was if they answered a question
        # Get the users answer
        user_answer = slack_payload_dict["actions"][0]["value"]
        # Get the question id from the action
        question_id = slack_payload_dict["callback_id"]
        # Find the question
        question = quiz.find_quiz_question(question_id)
        # Was the user answer correct
        is_correct = question.get("correct_answer") == user_answer

        # Get previous message attachment
        original_message_attachment = slack_payload_dict["original_message"]["attachments"][0]

        logger.debug(f"Original Message Attachment: {original_message_attachment}")

        updated_message_attachment = quiz.update_question_attachment(original_message_attachment,
                                                                     question.get("correct_answer"), is_correct)

        logger.debug(f"Updated Message Attachment: {updated_message_attachment}")

        logger.debug("Updating users score")

        user_streak = quiz.get_user_streak(user_id)

        messaging.send_answered_question(
            slack_client=sc,
            channel_id=channel_id,
            user_id=user_id,
            correct=is_correct,
            streak=user_streak
        )

        messaging.update_answered_question(
            slack_client=sc,
            channel_id=channel_id,
            ts=previous_action_ts,
            question_attachment=updated_message_attachment
        )

        # Update the users score
        quiz.update_user_score(user_id, is_correct)

        # Ask if the user wants to play again.
        messaging.ask_user_to_play_again(
            slack_client=sc,
            channel_id=channel_id,
            play_again_attachment=quiz.form_another_question_attachment()
        )

    # Everything went fine return a good response.
    return helpers.form_response(200)
