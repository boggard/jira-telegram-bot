from peewee import SqliteDatabase

db = SqliteDatabase('jira.db')

from model.user import User
from model.chat import Chat


def init_database():
    db.connect()
    db.create_tables(
        [User, Chat], True)
