from peewee import CharField, DateField, IntegerField, ForeignKeyField, TextField, DateTimeField, BooleanField
from helpers.models import BaseModel
import datetime

from user.models import User


class Wish(BaseModel):
    user = ForeignKeyField(User, on_delete='cascade', related_name='wishes')
    title = CharField(max_length=50)
    description = TextField()
    image = CharField()
    link = CharField(max_length=250)
    cost = IntegerField()
    balance = IntegerField()
    donator = ForeignKeyField(User, on_delete='SET NULL', related_name='wishes')
    creationdate = DateField(default=datetime.datetime.today())
    expiry = DateField(default=None)
    category = CharField(max_length=50)
    status = CharField(max_length=3)
    isHidden = BooleanField()
    from_user = ForeignKeyField(User, on_delete='CASCADE', related_name='wishes')

    def serialize(self):
        return {"id": self.id,
                "title": self.title,
                "description": self.description,
                "image": self.image,
                "href": self.href,
                "cost": self.cost
                }


class Comments(BaseModel):
    user = ForeignKeyField(User, on_delete='cascade', related_name='comments')
    wish = ForeignKeyField(Wish, on_delete='cascade', related_name='comments')
    time = DateTimeField(default=datetime.datetime.now)
    text = TextField()


Comments.response = ForeignKeyField(Comments, on_delete='cascade', related_name='response')


class ExcludeHidden:
    wish = ForeignKeyField(Wish, on_delete='cascade')
    user = ForeignKeyField(User, on_delete='cascade')