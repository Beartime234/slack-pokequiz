from boto3 import Session
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import logging
from sys import exit

from pokequiz.database.exceptions import CouldNotFindValue

logger = logging.getLogger(__name__)


class BaseDynamoTable(object):

    def __init__(self, boto_session: Session, table_name: str, quiz_id: str, primary_key: str, range_key: str):
        self._boto_session = boto_session
        self.table_name = table_name
        self.quiz_id = quiz_id
        self.primary_key = primary_key
        self.range_key = range_key
        _dynamodb = self._boto_session.resource('dynamodb')
        self._dynamo_db_table = _dynamodb.Table(self.table_name)

    def get_value(self, range_value: str):
        """Gets a value from the database based on the range key

        Args:
            range_value: The value of the range key.

        Returns:
            Gets an item from the database
        """
        get_value_response = self._dynamo_db_table.query(
            KeyConditionExpression=Key(self.primary_key).eq(self.quiz_id) &
                                   Key(self.range_key).eq(range_value),
            Limit=1
        )
        if len(get_value_response["Items"]) == 0:
            raise CouldNotFindValue(f"Could not find value with {range_value}")
        return get_value_response["Items"][0]

    def put_value(self, value):
        """Puts a value into the table. Will update if it already exits

        Args:
            value: The value you wish to put in the database
        """
        self._dynamo_db_table.put_item(
            Item=value
        )
