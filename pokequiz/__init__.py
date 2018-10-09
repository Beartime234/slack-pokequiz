"""Initializes Pokequiz and gets all the information it needs to run.

This probably shouldn't be in __init__ but because the application shares helpers and creates 2 lambda functions
from the same package this seems like the easiest method. Should probably be reworked into 2 different SRC folders.
"""

import time
import os
import boto3
import json
import logging.config
import yaml

__version__ = "0.1"

# Gets the real path of this location just so we can
dir_path = os.path.dirname(os.path.realpath(__file__))

# Read the logging configuration and set it
with open(f"{dir_path}/quiz_config/logging.yml", "rt") as f:
    config = yaml.safe_load(f.read())
    f.close()

logging.config.dictConfig(config)
logger = logging.getLogger(__name__)

# Ignore non important logs from botocore and boto3 cause they noisy as hell
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

logger.info(f"Starting up Quiz v{__version__}")
logger.debug("Starting initialization. Loading secrets and environment variables.")

# Get Environment Variables
# This is declared globally because as this is useful for all parts of the function
start_time = time.time()

QUIZ_ID = os.environ["QUIZ_ID"]

# Grab secrets for the application.
SECRETS_NAME = os.environ["SECRETS_NAME"]

client = boto3.client(
    service_name='secretsmanager'
)

get_secret_value_response = client.get_secret_value(
    SecretId=SECRETS_NAME
)

secret_value = get_secret_value_response["SecretString"]

# Load them into a dictionary
SECRETS = json.loads(secret_value)


# Check its a dictionary if it's not its probably an error
if type(SECRETS) is not dict:
    raise TypeError("Secrets must be a well formed dictionary.")

logger.debug(f"Loaded secrets successfully. Secrets: {SECRETS}.")

# Load the stage
STAGE = os.environ["STAGE"]

logger.debug(f"Loaded stage successfully. Stage: {STAGE}")

QUIZ_QUESTION_TABLE = os.environ["QUIZ_QUESTION_TABLE"]

QUIZ_LEADERBOARD_TABLE = os.environ["QUIZ_LEADERBOARD_TABLE"]

logger.debug(f"Loaded table variables successfully."
             f" Questions: {QUIZ_QUESTION_TABLE}, Leaderboard: {QUIZ_LEADERBOARD_TABLE}")

logger.debug("Startup Time: --- %s seconds ---" % (time.time() - start_time))
logger.debug("Initialization Successful")
