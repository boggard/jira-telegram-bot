class Comment:
    def __init__(self, jira_comment):
        self.author = jira_comment["author"]["displayName"]
        self.content = jira_comment["body"]
