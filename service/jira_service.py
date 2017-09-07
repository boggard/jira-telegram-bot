import requests
from model.issue import Issue
from model.user import User
from peewee import fn, IntegrityError
from config import JIRA_USER, JIRA_PASSWORD, JIRA_REST_URL, JIRA_WEB_URL
from utils import date_util

auth = (JIRA_USER, JIRA_PASSWORD)


def get_new_issues(username):
    user = User.get(name=username)
    last_date = Issue.select(fn.Max(Issue.updated)).where(Issue.user == user).get().updated
    last_date = date_util.to_jira_format(last_date) if last_date is not None else None
    url = JIRA_REST_URL + "/search?jql=assignee=" + username + \
          (" and updated>\'" + last_date + "\'" if last_date is not None else '') + \
          "+order+by+updated+asc"

    r = requests.get(url, auth=auth)

    return add_issues(r.json()["issues"], user=user)


def init_user_issues(user):
    url = JIRA_REST_URL + "/search?jql=assignee=" + user.name + "+order+by+created&maxResults=1"

    r = requests.get(url, auth=auth)

    add_issues(r.json()["issues"], user=user)


def add_issues(*issues, user):
    db_issues = []
    for issue in issues[0]:
        jira_id = issue["id"]
        created = date_util.format_jira_date(issue["fields"]["created"])
        updated = date_util.format_jira_date(issue["fields"]["updated"])
        db_issue = None

        try:
            db_issue = Issue.create(jira_id=jira_id, user=user)
        except IntegrityError:
            db_issue = Issue.get(jira_id=jira_id)
            if date_util.to_db_format(db_issue.updated) == updated:
                continue
        db_issue.created = created
        db_issue.updated = updated
        db_issue = edit_issue(db_issue, issue)
        db_issue.save()
        db_issues.append(db_issue)

    return db_issues


def edit_issue(db_issue, jira_issue):
    db_issue.caption = jira_issue["fields"]["summary"]
    db_issue.project_name = jira_issue["fields"]["project"]["name"]
    db_issue.alias = jira_issue["key"]
    db_issue.link = JIRA_WEB_URL + "browse/" + jira_issue["key"]
    db_issue.description = jira_issue["fields"]["description"]
    db_issue.author = jira_issue["fields"]["reporter"]["displayName"]
    return db_issue
