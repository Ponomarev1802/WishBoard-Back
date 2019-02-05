from aiohttp import web
from .models import User, Followers
from helpers.tools import redirect
from peewee import fn, JOIN

from helpers.decorators import login_required


class GetUser(web.View):
    @login_required
    async def get(self):
        user = self.request.user
        id = self.request.rel_url.query.get('id', user.id)
        print(id)
        if id==user.id:
            return {"user": user.serialize()}
        else:
            return {}


class AddUser(web.View):
    async def post(self):
        data = self.request.data
        #print(data)
        try:
            user = await self.request.app.objects.create(User, **data)
        except:
            self.request.status.update({"err": "регистрация не удалась"})
        return {}


class LoginUser(web.View):
    async def post(self):
        data = self.request.data
        user = False
        #print (data)
        try:
            user = await self.request.app.objects.get(User, **data)
        except:
            self.request.status.update({"req": False})
        if user:
            self.request.session['user'] = str(user.id)
            redirect(self.request, 'GetUser')
        self.request.status.update({"err": "Логин и пароль не совпадают"})
        return {}


class Subscribe(web.View):
    async def post(self):
        toward = self.request.data.toward
        user = self.request.user
        try:
            await self.request.app.objects.create(Followers, toward, user.id)
        except:
            self.request.status.update({"err": "Не удалось подписаться"})
        return {}