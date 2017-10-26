from config import JIRA_WEB_URL
from utils import date_util
from utils.markdown import markdown_prepare


class Issue:
    def __init__(self, jira_issue, comments):
        self.created = date_util.to_str(
            date_util.format_jira_date(jira_issue["fields"].get("created")))
        self.updated = date_util.to_str(
            date_util.format_jira_date(jira_issue["fields"].get("updated")))
        self.caption = jira_issue["fields"].get("summary")
        self.project_name = jira_issue["fields"]["project"].get("name")
        self.alias = jira_issue["key"]
        self.link = JIRA_WEB_URL + "browse/" + jira_issue["key"]
        self.description = jira_issue["fields"].get("description") or ""
        self.author = jira_issue["fields"]["reporter"].get("displayName")
        assignee = jira_issue["fields"].get("assignee")
        self.assignee = assignee[
            "displayName"] if assignee is not None else "Not defined"
        self.status = jira_issue["fields"]["status"].get("name") or ""
        self.components = ",".join([component["name"] for component in
                                    jira_issue["fields"]["components"]])
        self.comments = comments

    def get_info(self):
        text = ["*Project*: {}".format(markdown_prepare(self.project_name))]
        if self.created == self.updated:
            text.append(
                "*Issue*: [{}]({}) *was created* on *{}*".format(self.alias,
                                                                 self.link,
                                                                 self.created))
        else:
            text.append(
                "*Issue*: [{}]({}) *was updated* on *{}*".format(self.alias,
                                                                 self.link,
                                                                 self.updated))
        text.append(
            "*Components*: {}".format(markdown_prepare(self.components)))
        text.append(
            "*Status*: {}".format(markdown_prepare(self.status)))
        text.append(
            "*Author*: {}".format(markdown_prepare(self.author)))
        text.append(
            "*Assignee*: {}".format(markdown_prepare(self.assignee)))
        text.append(
            "*Caption*: {}".format(markdown_prepare(self.caption)))
        text.append(
            "*Description*: {}".format(markdown_prepare(self.description)))
    
        if self.comments:
            text.append("\n*New comments*:")
            for comment in self.comments:
                text.append("*{}* said: {}".format(comment.author,
                                                   markdown_prepare(
                                                       comment.content)))
    
        return "".join(text)
