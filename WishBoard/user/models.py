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

class Wish(BaseModel):
    user = ForeignKeyField(User, on_delete='CASCADE', related_name='wishes')
    title = CharField(max_length=50)
    description = TextField()
    image = CharField()
    href = CharField(max_length=250)
    cost = IntegerField()
    balance = IntegerField()

    def serialize(self):
        return {"id": self.id,
                "title": self.title,
                "description": self.description,
                "image": self.image,
                "href": self.href,
                "cost": self.cost
                }
