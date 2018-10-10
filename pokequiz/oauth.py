"""
Slack chat-bot Lambda handler.
"""

# Module Imports
import logging
import json
from slackclient import SlackClient

# Local imports
from pokequiz import helpers, messaging, SECRETS, QUIZ_ID

# Import the quiz
from pokequiz.quiz import Quiz

logger = logging.getLogger(__name__)


def lambda_handler(api_event, api_context):
    """Handle an incoming HTTP request from a Slack chat-bot.
    """
    logger.debug(f"Api Event: {api_event}")

    # Grab relevant information form the api_event
    query_string_params = api_event["queryStringParameters"]
    request_headers = api_event["headers"]

    oauth_code = query_string_params["code"]

    # Build the slack client. This allows us make slack API calls
    # read up on the python-slack-client here. We get this from
    # AWS secrets manager. https://github.com/slackapi/python-slackclient
    sc = SlackClient(SECRETS["BOT_TOKEN"])

    messaging.send_oauth_response(sc, SECRETS["CLIENT_ID"], SECRETS["CLIENT_SECRET"], oauth_code)

    logger.info("Returning successful response.")
    # Everything went fine return a good response.
    return helpers.form_response(200, {"message": "Auth Successful"})
