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
config_dir_name = "config"
LOGGING_CONFIG_FILENAME = "logging.yml"
APP_CONFIG_FILENAME = "app.yml"

# Gets the real path of this location just so we can
dir_path = os.path.dirname(os.path.realpath(__file__))

# Read the logging configuration and set it
with open(f"{dir_path}/{config_dir_name}/{LOGGING_CONFIG_FILENAME}", "rt") as f:
    app_config = yaml.safe_load(f.read())
    f.close()

logging.config.dictConfig(app_config)
logger = logging.getLogger(__name__)

# Ignore non important logs from botocore and boto3 cause they noisy as hell
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

# Read the application config
with open(f"{dir_path}/{config_dir_name}/{APP_CONFIG_FILENAME}", "rt") as f:
    app_config = yaml.safe_load(f.read())
    f.close()

logger.info(f"Starting up Quiz v{__version__}")
logger.debug("Starting initialization. Loading secrets and environment variables.")

# Get Environment Variables
# This is declared globally because as this is useful for all parts of the function
start_time = time.time()

# Get the QUIZ_ID and load the configuration for it
QUIZ_ID = os.environ["QUIZ_ID"]

# Get the Quiz Config
QUIZ_CONFIG = app_config["quiz"]
MESSAGING_CONFIG = app_config["messaging"]
OAUTH_CONFIG = app_config["oauth"]

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

if SECRETS is None:
    raise TypeError("Secrets should not be None")

logger.debug(f"Loaded secrets successfully. Secrets: {SECRETS}.")

# Load the stage
STAGE = os.environ["STAGE"]

logger.debug(f"Loaded stage successfully. Stage: {STAGE}")

QUIZ_STORAGE_TABLE = os.environ["QUIZ_STORAGE_TABLE"]

logger.debug(f"Loaded table variables successfully."
             f" StorageTable: {QUIZ_STORAGE_TABLE}")

logger.debug("Startup Time: --- %s seconds ---" % (time.time() - start_time))
logger.debug("Initialization Successful")
