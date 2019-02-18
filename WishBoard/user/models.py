from peewee import CharField, DateField, IntegerField, ForeignKeyField, TextField,fn, JOIN, SelectQuery
from helpers.models import BaseModel
import datetime
import json


class User(BaseModel):
    name = CharField(max_length=30)
    surename = CharField(max_length=30, null=True)
    nickname = CharField(max_length=30, unique=True, index=True)
    email = CharField(max_length=50, unique=True, index=True)
    password = CharField()
    photo = CharField(null=True)
    birth_date = DateField(null=True)
    last_visit = DateField(default=datetime.datetime.today())
    session_key = CharField(max_length=100, null=True)

    def serialize(self):
        return {"name": self.name,
                "surename": self.surename,
                "nickname": self.nickname,
                "photo": self.photo,
                "birth_date": str(self.birth_date),
                "followers": self.flwrs if hasattr(self, 'flwrs') else 0,
                "follows": self.flws if hasattr(self, 'flws') else 0,
                }

    @classmethod
    def getAll(cls, id):
        Followers1 = Followers.alias()
        query = (User.select(User,
                             fn.COUNT(fn.DISTINCT(Followers.id)).alias('flws'),
                             fn.COUNT(fn.DISTINCT(Followers1.id)).alias('flwrs'))
                 .join(Followers, JOIN.LEFT_OUTER, on=Followers.whom==User.id)
                 .join(Followers1, JOIN.LEFT_OUTER, on=Followers1.toward==User.id)
                 .where(User.id == id)
                 .group_by(User.id)
                 )
        return query

class Followers(BaseModel):
    toward = ForeignKeyField(User, on_delete="CASCADE", related_name="followers")
    whom = ForeignKeyField(User, on_delete="CASCADE", related_name="follows")
    class Meta:
        #unique = ("toward_id", "whom_id")
        indexes = (
            (("toward", "whom"), True),
        )


"""
Запрос на получение пользователя с количеством его подписок и подсписчиков
SELECT *, (SELECT COUNT(*) FROM followers WHERE followers.toward_id=11) AS FOLLOWERS
,(SELECT COUNT(*) FROM followers WHERE followers.whom_id=11) AS FOLLOWERS
FROM "user"




SELECT a.id, COUNT(r.toward_id) as followers, count (s.whom_id) as follows
FROM "user" a
JOIN followers r
ON a.id = r.toward_id
JOIN followers s
ON a.id = s.whom_id
   WHERE a.id = 11
GROUP BY a.id

"""

"""
Запрос на получение пользователя с количеством его подписок и подсписчиков
SELECT a.id, COUNT(r.toward_id) as followers, count (s.whom_id) as follows
            FROM "user" a
            JOIN followers r
              ON a.id = r.toward_id
            JOIN followers s
              ON a.id = s.whom_id
            WHERE a.id = 11
            GROUP BY a.id
"""