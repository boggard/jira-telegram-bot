from peewee import SqliteDatabase

db = SqliteDatabase('jira.db')

from model.issue import Issue
from model.user import User
from model.chat import Chat


def init_database():
    db.connect()
    db.create_tables(
        [User, Issue, Chat], True)
