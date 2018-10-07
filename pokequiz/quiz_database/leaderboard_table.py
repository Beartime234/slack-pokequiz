import logging
from boto3 import Session

from pokequiz.quiz_database.base_dynamo_table import BaseDynamoTable
from pokequiz.quiz_database.exceptions import CouldNotFindValue


logger = logging.getLogger(__name__)


class LeaderboardTable(BaseDynamoTable):
    """Leaderboard Table Class for performing actions to the leaderboard database
    """
    def __init__(self, boto_session: Session, table_name: str, quiz_id: str, primary_key: str, range_key: str,
                 team_id: str):
        super().__init__(boto_session, table_name, quiz_id, primary_key, range_key)
        self.team_id: str = team_id
        try:
            self._table_value = self.get_value(team_id)
        except CouldNotFindValue:
            self.initialize_new_team(team_id)

    def initialize_new_team(self, team_id: str):
        """Initializes a new team if they have never had a value before

        Args:
            team_id: The teams id
        """
        self.put_value(
            {
                "quizId": self.quiz_id,
                "teamRange": team_id
            }
        )
        self._table_value = self.get_value(team_id)
        return

    def initialize_new_user(self, user_id: str):
        """Initializes a new user if they have never had a value in the database before

        Args:
            user_id: The users id
        """
        try:
            self._table_value["user_scores"][user_id] = {
                "overall_score": 0,
                "streak": 0
            }
            self.put_value(self._table_value)
        except KeyError:
            self.initialize_first_user(user_id)
            return
        return

    def initialize_first_user(self, user_id):
        """Initializes the first user in the database if it was a new team

        Args:
            user_id: The user's id
        """
        self._table_value["user_scores"] = {
            user_id: {
                "overall_score": 0,
                "streak": 0
            }
        }
        self.put_value(self._table_value)
        return

    def save_team_score_dict(self):
        """Saves the teams score in the database
        """
        self.put_value(self._table_value)
        return

    def save_correct_answer(self, user_id: str, increase_value: int):
        """Saves the users score in the database if they got the correct answer

        Args:
            user_id: The users id
            increase_value: The value to increase it by
        """
        try:
            self._table_value["user_scores"][user_id]["overall_score"] += increase_value
            self._table_value["user_scores"][user_id]["streak"] += 1
            self.save_team_score_dict()
        except KeyError:
            self.initialize_new_user(user_id)
            self.save_correct_answer(user_id, increase_value)

    def save_incorrect_answer(self, user_id: str, decrease_value: int):
        """Saves the users score in the database if they got the correct answer

        Args:
            user_id: The users id
            decrease_value: The value to decrease it by
        """
        try:
            self._table_value["user_scores"][user_id]["overall_score"] += decrease_value
            self._table_value["user_scores"][user_id]["streak"] = 0
            self.save_team_score_dict()
        except KeyError:
            self.initialize_new_user(user_id)
            self.save_incorrect_answer(user_id, decrease_value)

    def get_user_scores(self) -> dict:
        """Returns all the users scores from the leaderboard database

        Returns: A dictionary of all values in the database
        """
        return self._table_value["user_scores"]

    def get_user_score(self, user_id: str) -> dict:
        """Gets a specific user score from the database

        Args:
            user_id: The users id

        Returns:
            A dictionary with the users score and streak
        """
        return self._table_value["user_scores"][user_id]

    def get_user_streak(self, user_id: str) -> int:
        """Gets a specific users streak from the database
        Args:
            user_id: The users id

        Returns:
            An integer of their overall score
        """
        return self.get_user_score(user_id)["streak"]

    def get_user_overall_score(self, user_id: str) -> int:
        """Gets a specific users overall score from the database

        Args:
            user_id: The users id

        Returns:
            An integer of the users overall score
        """
        return self.get_user_score(user_id)["overall_score"]
