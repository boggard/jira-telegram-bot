from peewee import *
from model.abstract_entity import AbstractEntity
from utils.date_util import DB_FORMAT


class User(AbstractEntity):
    id = PrimaryKeyField()
    name = CharField(unique=True)
    last_updated = DateTimeField(null=True, formats=[DB_FORMAT])
