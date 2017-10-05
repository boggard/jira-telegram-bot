from config import JIRA_WEB_URL
from utils import date_util
from utils.markdown import markdown_prepare


class Issue:
    def __init__(self, jira_issue, comments):
        self.created = date_util.to_str(date_util.format_jira_date(jira_issue["fields"].get("created")))
        self.updated = date_util.to_str(date_util.format_jira_date(jira_issue["fields"].get("updated")))
        self.caption = jira_issue["fields"].get("summary")
        self.project_name = jira_issue["fields"]["project"].get("name")
        self.alias = jira_issue["key"]
        self.link = JIRA_WEB_URL + "browse/" + jira_issue["key"]
        self.description = jira_issue["fields"].get("description", "")
        self.author = jira_issue["fields"]["reporter"].get("displayName")
        assignee = jira_issue["fields"].get("assignee")
        self.assignee = assignee["displayName"] if assignee is not None else "Not defined"
        self.status = jira_issue["fields"]["status"].get("name", "")
        self.components = ",".join([component["name"] for component in jira_issue["fields"]["components"]])
        self.comments = comments

    def __str__(self):
        text = "*Project*: " + markdown_prepare(self.project_name) + "\n" + \
               "*Issue*: [" + self.alias + "]" + "(" + self.link + ")" + \
               (" *was created* on *" + self.created + "*" if self.created == self.updated
                else " *was updated* on *" + self.updated + "*") + "\n" + \
               "*Components*: " + markdown_prepare(self.components) + "\n" + \
               "*Status*: " + markdown_prepare(self.status) + "\n" + \
               "*Author*: " + markdown_prepare(self.author) + "\n" + \
               "*Assignee*: " + markdown_prepare(self.assignee) + "\n" + \
               "*Caption*: " + markdown_prepare(self.caption) + "\n" + \
               "*Description*: " + markdown_prepare(self.description) + "\n"

        if len(self.comments) > 0:
            text += "\n" + "*New comments*: " + "\n" + \
                    "\n".join("*" + comment.author + " said*: " + markdown_prepare(comment.content)
                              for comment in self.comments)

        return text
