import requests

from config import JIRA_USER, JIRA_PASSWORD, JIRA_REST_URL
from dto.comment import Comment
from dto.issue import Issue
from model.user import User
from utils import date_util

auth = (JIRA_USER, JIRA_PASSWORD)


def get_new_issues(username):
    user = User.get(User.name == username)
    last_date = user.last_updated
    last_date = date_util.to_jira_format(last_date) if last_date is not None else None
    url = JIRA_REST_URL + "/search?jql=(assignee=" + username + \
                          " or reporter=" + username + " or watcher=" + username + ")" + \
                          (" and updated>\'" + last_date + "\'" if last_date is not None else '') + \
                          "+order+by+updated+asc"

    r = requests.get(url, auth=auth)

    return get_issues(r.json()["issues"], user=user)


def get_issues(*issues, user: User):
    issues_wrappers = []
    for issue in issues[0]:
        updated = date_util.format_jira_date(issue["fields"]["updated"])

        if user.last_updated is None or user.last_updated < updated:
            user.last_updated = updated
            user.save()
            if not is_own_update(issue, user.name):
                issues_wrappers.append(Issue(issue, get_comments(issue)))

    return issues_wrappers


def get_comments(issue):
    url = JIRA_REST_URL + "/issue/" + issue["id"] + "/comment"

    r = requests.get(url, auth=auth)

    return [Comment(comment) for comment in r.json()["comments"]
            if date_util.format_jira_date(comment["updated"]) == date_util.format_jira_date(issue["fields"]["updated"])]


def is_own_update(issue, username: str):
    url = JIRA_REST_URL + "/issue/" + issue["key"]

    response = requests.get(url, params={"expand": "changelog"}, auth=auth)

    histories = response.json()["changelog"]["histories"]

    if len(histories) == 0:
        return issue["fields"]["reporter"]["key"] == username
    else:
        return histories[-1]["author"]["key"] == username
