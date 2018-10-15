import logging
import json
import urllib
import time
import hmac
import hashlib
from pokequiz import STAGE

# Set up logging here
logger = logging.getLogger(__name__)

# Define the URL of the targeted Slack API resource.
SLACK_URL = "https://slack.com/api/chat.postMessage"


def form_response(status_code: int, body: dict = None, additional_headers: dict = None):
    """Generates a JSON response

    Args:
        additional_headers: Any additionaal headers you wish to add
        status_code (int): A integer of the applicable status code
        body (dict): A dictionary to send as a response.

    Returns:
        A properly formed response
    """

    # Fixes it for a blank response doesn't update interactive messages
    if additional_headers is None:
        additional_headers = {}
    headers = {
        "Content-Type": "application/json"
    }
    headers.update(additional_headers)
    if body is None:
        return {
            "isBase64Encoded": True,
            "statusCode": status_code,
            "headers": headers
        }
    return {
        "isBase64Encoded": True,
        "statusCode": status_code,
        "headers": headers,
        "body": json.dumps(body)
    }


def send_slack_request(data: dict, bot_token: str, request_method: str = "POST"):
    """ Sends a request to the slack API. This sends it manually using urllib but you should use the slack
    client defined in the app.py.

    Args:
        data: A dictionary of the json data you would like to send
        bot_token: The secret bot token that authroizes the app to send it as that bot
        request_method: The request method. Default: POST
    """

    # First dump the data into a string and encode it as bytes as this is necessary
    data = json.dumps(data).encode('utf-8')

    # Add headers specifying that we are sending a JSON response
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {bot_token}"
    }

    # Construct the HTTP request that will be sent to the Slack API.
    request = urllib.request.Request(
        SLACK_URL,
        data=data,
        method=request_method,
        headers=headers
    )

    # Fire off the request!
    urllib.request.urlopen(request).read()
    return


def is_challenge(slack_event_body: dict) -> bool:
    """Is the event a challenge from slack? If yes return the correct response to slack

    Args:
        slack_event_body (dict): The slack event JSON

    Returns:
        returns True if it is a slack challenge event returns False otherwise
    """
    if "challenge" in slack_event_body:
        logger.info(f"Challenge Data: {slack_event_body['challenge']}")
        return True
    return False


def verify_request(request_headers: dict, slack_event_body: str, app_signing_secret) -> bool:
    """Does the header sent in the request match the secret token.

    If it doesn't it may be an insecure request from someone trying to pose as your
    application. You can read more about the url-verification and why this is necessary
    here https://api.slack.com/docs/verifying-requests-from-slack

    Args:
        app_signing_secret (str): The apps local signing secret that is given by slack to compare with formulated.
        request_headers (dict): The request headers, must contain X-Slack-Signature and X-Slack-Request-Timestamp
        slack_event_body (str): The slack event body that must be formulated as a string

    Returns:
        A boolean. If True the request was valid if False request was not valid.
    """

    # If the stage is production then continue if not do some checks
    if STAGE != "prod":
        logger.debug(f"We are not in production. So we aren't going to verify the request.")
        return True
    logger.debug(f"Verifying request from slack.")
    slack_signature = request_headers["X-Slack-Signature"]
    slack_timestamp = request_headers["X-Slack-Request-Timestamp"]
    # Is the request older then 5 minutes
    if abs(time.time() - float(slack_timestamp)) > 60 * 5:
        logger.warning(f"Request verification failed. Timestamp was over 5 min's old for the request")
        return False

    # Does the hash that we create match the hash that slack has sent?

    # Create the hash
    sig_basestring = f"v0:{slack_timestamp}:{slack_event_body}".encode('utf-8')
    slack_signing_secret = bytes(app_signing_secret, 'utf-8')
    my_signature = 'v0=' + hmac.new(slack_signing_secret, sig_basestring, hashlib.sha256).hexdigest()

    # Compare the hash
    if hmac.compare_digest(my_signature, slack_signature):
        return True
    else:
        logger.warning(f"Verification failed. my_signature: {my_signature} slack_signature: {slack_signature}")
        return False


def replace_user_id(replace_string: str, user_id):
    """Replaces text in a string with user id. String must be ${user_id}
    """
    slack_appropriate_user_id = f"<@{user_id}>"
    return replace_string.replace("${user_id}", slack_appropriate_user_id)


def replace_streak(replace_string: str, streak):
    """Replaces text in a string with streak. String must be ${streak}

    Also converts streak it to a string
    """
    streak = str(streak)
    print(f"REPLACE STRING = {replace_string}")
    print(f"STREAK = {streak}")
    final_string = replace_string.replace("${streak}", streak)
    print(f"FINAL STRING = {final_string}")
    return final_string


def replace_values(replace_string, user_id=None, streak=None):
    """Main controller for replacing values in the configuration file

    Args:
        streak:
        replace_string: The string you are looking for replacements in
        user_id:

    Returns:

    """
    if user_id is not None:
        replace_string = replace_user_id(replace_string, user_id)
    if streak is not None:
        replace_string = replace_streak(replace_string, streak)
    return replace_string
