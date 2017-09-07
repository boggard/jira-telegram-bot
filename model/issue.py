from peewee import *
from model.user import User
from model.abstract_entity import AbstractEntity
from utils.date_util import DB_FORMAT


class Issue(AbstractEntity):
    id = PrimaryKeyField()
    jira_id = IntegerField(unique=True)
    user = ForeignKeyField(User, related_name="issues")
    caption = CharField(null=True)
    created = DateTimeField(null=True, formats=[DB_FORMAT])
    updated = DateTimeField(null=True, formats=[DB_FORMAT])
    project_name = CharField(null=True)
    alias = CharField(null=True)
    link = CharField(null=True)
    description = CharField(null=True)
    author = CharField(null=True)
