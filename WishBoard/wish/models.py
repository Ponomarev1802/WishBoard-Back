from peewee import CharField, DateField, IntegerField, ForeignKeyField, TextField, DateTimeField, BooleanField
from helpers.models import BaseModel
import datetime

from user.models import User


class Wish(BaseModel):
    user = ForeignKeyField(User, on_delete='cascade', related_name='wishes', index=True)
    title = CharField(max_length=50)
    description = TextField(null=True)
    image = CharField(null=True)
    link = CharField(max_length=250, null=True)
    cost = IntegerField(null=True)
    balance = IntegerField(null=True)
    donator = ForeignKeyField(User, on_delete='SET NULL', related_name='donate_wishes', null=True, index=True)
    creationdate = DateField(default=datetime.datetime.today())
    expiry = DateField(null=True)
    category = CharField(max_length=50, null=True)
    status = CharField(max_length=3, null=True)
    isHidden = BooleanField(default=False)
    from_user = ForeignKeyField(User, on_delete='CASCADE', related_name='out_wishes', null=True)

    def serialize(self):
        return {"id": self.id,
                "title": self.title,
                "description": self.description,
                "image": self.image,
                "href": self.href,
                "cost": self.cost
                }


class Comments(BaseModel):
    user = ForeignKeyField(User, on_delete='cascade', related_name='comments', index=True)
    wish = ForeignKeyField(Wish, on_delete='cascade', related_name='comments', index=True)
    time = DateTimeField(default=datetime.datetime.now, index=True)
    text = TextField()
    #response = ForeignKeyField(Comments, on_delete='cascade', related_name='response')


class ExcludeHidden(BaseModel):
    wish = ForeignKeyField(Wish, on_delete='cascade', index=True)
    user = ForeignKeyField(User, on_delete='cascade')