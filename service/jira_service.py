import requests
from model.user import User
from config import JIRA_USER, JIRA_PASSWORD, JIRA_REST_URL
from utils import date_util
from dto.issue import Issue
from dto.comment import Comment

auth = (JIRA_USER, JIRA_PASSWORD)


def get_new_issues(username):
    user = User.get(name=username)
    last_date = user.last_updated
    last_date = date_util.to_jira_format(last_date) if last_date is not None else None
    url = JIRA_REST_URL + "/search?jql=(assignee=" + username + \
          " or reporter=" + username + ")" + \
          (" and updated>\'" + last_date + "\'" if last_date is not None else '') + \
          "+order+by+updated+asc"

    r = requests.get(url, auth=auth)

    return add_issues(r.json()["issues"], user=user)


def init_user_issues(user):
    url = JIRA_REST_URL + "/search?jql=assignee=" + user.name + "+order+by+created&maxResults=1"

    r = requests.get(url, auth=auth)

    add_issues(r.json()["issues"], user=user)


def add_issues(*issues, user: User):
    issues_wrappers = []
    for issue in issues[0]:
        updated = date_util.format_jira_date(issue["fields"]["updated"])

        if user.last_updated is None or user.last_updated < updated:
            user.last_updated = updated
            user.save()
            issues_wrappers.append(Issue(issue, get_comments(issue)))

    return issues_wrappers


def get_comments(issue):
    url = JIRA_REST_URL + "/issue/" + issue["id"] + "/comment"

    r = requests.get(url, auth=auth)

    return [Comment(comment) for comment in r.json()["comments"]
            if date_util.format_jira_date(comment["updated"]) == date_util.format_jira_date(issue["fields"]["updated"])]
