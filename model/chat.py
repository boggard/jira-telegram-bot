from peewee import *
from model.abstract_entity import AbstractEntity
from model.user import User


class Chat(AbstractEntity):
    id = PrimaryKeyField()
    t_id = IntegerField(unique=True)
    user = ForeignKeyField(User, related_name="chats", null=True)
