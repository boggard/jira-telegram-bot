from config import JIRA_WEB_URL
from utils import date_util


class Issue:
    def __init__(self, jira_issue):
        self.created = date_util.to_str(date_util.format_jira_date(jira_issue["fields"]["created"]))
        self.updated = date_util.to_str(date_util.format_jira_date(jira_issue["fields"]["updated"]))
        self.caption = jira_issue["fields"]["summary"]
        self.project_name = jira_issue["fields"]["project"]["name"]
        self.alias = jira_issue["key"]
        self.link = JIRA_WEB_URL + "browse/" + jira_issue["key"]
        self.description = jira_issue["fields"]["description"]
        self.author = jira_issue["fields"]["reporter"]["displayName"]
        assignee = jira_issue["fields"]["assignee"]
        self.assignee = assignee["displayName"] if assignee is not None else "Not defined"
        self.status = jira_issue["fields"]["status"]["name"]
        self.components = ",".join([component["name"] for component in jira_issue["fields"]["components"]])
