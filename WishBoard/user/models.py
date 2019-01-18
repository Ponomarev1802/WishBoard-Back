from peewee import CharField, DateField, IntegerField, ForeignKeyField, TextField
from helpers.models import BaseModel
import json


class User(BaseModel):
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    email = CharField(max_length=50)
    password = CharField()
    photo = CharField()
    birth_date = DateField()

    def serialize(self):
        return {"first_name": self.first_name,
                "last_name": self.last_name,
                "photo": self.photo,
                "birth_date": str(self.birth_date),
                }

class Wish(BaseModel):
    user = ForeignKeyField(User, on_delete='CASCADE', related_name='wishes')
    title = CharField(max_length=50)
    description = TextField()
    image = CharField()
    href = CharField(max_length=250)
    cost = IntegerField()
    balance = IntegerField()

    def serialize(self):
        return {"title": self.title,
                "description": self.description,
                "image": self.image,
                "href": self.href,
                "cost": self.cost
                }
