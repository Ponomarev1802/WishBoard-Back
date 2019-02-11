from peewee import CharField, DateField, IntegerField, \
    ForeignKeyField, TextField, DateTimeField, \
    BooleanField, JOIN
from helpers.models import BaseModel
import datetime
from peewee import fn
import json

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
                "link": self.link,
                "cost": self.cost
                }
    @classmethod
    def GetFull(cls, id):
        query = (Wish.select(Wish,
                             Comments.id.alias('Cid'), Comments.text.alias('Ctext'),
                             Comments.user.alias('Cuser'), Comments.time.alias('Ctime'),
                             fn.ARRAY_AGG(ExcludeHidden.user).alias('Exclude'))
                 .join(Comments, JOIN.LEFT_OUTER, on=Comments.wish == Wish.id)
                 .join(ExcludeHidden, JOIN.LEFT_OUTER, on=ExcludeHidden.wish == Wish.id)
                 .where(Wish.id == id)
                 .group_by(Wish.id, Comments.id)
                 )
        print(query)
        return query


class Comments(BaseModel):
    user = ForeignKeyField(User, on_delete='cascade', related_name='comments', index=True)
    wish = ForeignKeyField(Wish, on_delete='cascade', related_name='comments', index=True)
    time = DateTimeField(default=datetime.datetime.now, index=True)
    text = TextField()
    #response = ForeignKeyField(Comments, on_delete='cascade', related_name='response')


class ExcludeHidden(BaseModel):
    wish = ForeignKeyField(Wish, on_delete='cascade', index=True, related_name="exclude")
    user = ForeignKeyField(User, on_delete='cascade')
    class Meta:
        #unique = ("toward_id", "whom_id")
        indexes = (
            (("wish", "user"), True),
        )