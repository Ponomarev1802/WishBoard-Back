from peewee import CharField, DateField, IntegerField, ForeignKeyField, TextField
from helpers.models import BaseModel

from user.models import User


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
