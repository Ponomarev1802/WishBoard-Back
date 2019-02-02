from peewee import CharField, DateField, IntegerField, ForeignKeyField, TextField
from helpers.models import BaseModel
import json


class User(BaseModel):
    name = CharField(max_length=30)
    surename = CharField(max_length=30, null=True)
    email = CharField(max_length=50, unique=True)
    password = CharField()
    photo = CharField(null=True)
    birth_date = DateField(null=True)

    def serialize(self):
        return {"name": self.name,
                "surename": self.surename,
                "photo": self.photo,
                "birth_date": str(self.birth_date),
                }