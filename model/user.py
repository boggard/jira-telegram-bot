from peewee import *
from model.abstract_entity import AbstractEntity


class User(AbstractEntity):
    id = PrimaryKeyField()
    name = CharField(unique=True)
    last_updated = DateTimeField(null=True)
