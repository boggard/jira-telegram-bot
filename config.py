import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

TOKEN = os.environ["TOKEN"]
PROXY_URL = os.environ["PROXY_URL"]
JIRA_REST_URL = os.environ["JIRA_REST_URL"]
JIRA_WEB_URL = os.environ["JIRA_WEB_URL"]
JIRA_USER = os.environ["JIRA_USER"]
JIRA_PASSWORD = os.environ["JIRA_PASSWORD"]
PROC_TITLE = os.environ["PROC_TITLE"]
JIRA_REQUESTS_SECONDS_PERIOD = os.environ["JIRA_REQUESTS_SECONDS_PERIOD"]
LOG_ERROR_FILE = os.environ["LOG_ERROR_FILE"]