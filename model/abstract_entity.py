from peewee import Model
from model import db


class AbstractEntity(Model):
    class Meta:
        database = db
