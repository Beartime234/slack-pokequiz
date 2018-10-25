import logging
import random
from uuid import uuid4
from boto3 import Session
from boto3.dynamodb.conditions import Key

from pokequiz.database.base_table import BaseDynamoTable
from pokequiz.database.exceptions import CouldNotFindValue

logger = logging.getLogger(__name__)


class QuizQuestionTable(BaseDynamoTable):
    def __init__(self, boto_session: Session, table_name: str, quiz_id: str, primary_key: str, range_key: str):
        super().__init__(boto_session, table_name, quiz_id, primary_key, range_key)

    def get_random_value(self):
        """Gets a random value from the database.

        Requires a database with a table with a UUID as the range key. This
        function generates a new UUID then looks if there are any ids that are greater then it.
        If it cannot find one it will then check if any are lower. As more questions are added
        this function should theoretically get faster as it will only do the greater then check.

        Returns:
            dict: A dictionary of the data in the dynamo db table
        """

        # Get a uuid to compare with the range key on the table.
        # By limiting it to 1 we create a way to randomly query a dynamo db table
        comparing_uuid = str(uuid4())

        # First check if the uuid is greater then any in the table. Will actually return 3 responses and pick a
        # random value from there. This is to create more variation in question otherwise there will be gaps
        # frequently. In the way uuids are compared. This theoretically only will use 1 read capacity
        get_value_gt_response = self._dynamo_db_table.query(
            KeyConditionExpression=Key(self.primary_key).eq(self.quiz_id) & Key(self.range_key).gt(comparing_uuid),
            Limit=5
        )

        # If there is a response return it
        if len(get_value_gt_response["Items"]) > 0:
            return random.choice(get_value_gt_response["Items"])  # This is so questions that have a similar id still
            #  have a chance and increases randomness

        # If not then something has to be lower then it otherwise there wont be any in the table
        get_value_lt_response = self._dynamo_db_table.query(
            KeyConditionExpression=Key(self.primary_key).eq(self.quiz_id) & Key(self.range_key).lt(comparing_uuid),
            Limit=1
        )

        # Raise an error if we can't find any questions lower or greater then
        if len(get_value_lt_response["Items"]) == 0:
            raise CouldNotFindValue("Could not find a random question. Are there any questions in the database?")

        # Returns the first item as we should be only getting one value due to limit
        return get_value_lt_response["Items"][0]
