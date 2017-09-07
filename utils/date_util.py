from datetime import datetime

JIRA_FORMAT = "%Y/%m/%d %H:%M"
DB_FORMAT = "%Y/%m/%d %H:%M:%S"


def format_jira_date(date: str):
    return datetime.strptime(date[0:19], "%Y-%m-%dT%H:%M:%S").strftime(DB_FORMAT)


def to_jira_format(date: datetime):
    return date.strftime(JIRA_FORMAT)


def to_db_format(date: datetime):
    return date.strftime(DB_FORMAT)
