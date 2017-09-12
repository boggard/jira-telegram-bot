from peewee import *
from model.abstract_entity import AbstractEntity


class Permission(AbstractEntity):
    id = PrimaryKeyField()
    t_id = IntegerField(unique=True)
