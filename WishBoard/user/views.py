from aiohttp import web
from .models import User, Followers
from helpers.tools import redirect

from helpers.decorators import login_required


class GetUser(web.View):
    @login_required
    async def get(self):
        user = self.request.user
        id = self.request.rel_url.query.get('id', user.id)
        if id == user.id:
            return {"user": user.serialize()}
        else:
            try:
                user = await self.request.app.objects.get(User.getAll(id))
                return {"user": user.serialize()}
            except:
                return {"user": {}}

class Logout(web.View):
    async def post(self):
        self.request.session.pop('user')
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
            self.request.status.update({"err": "Логин и пароль не совпадают"})
        if user:
            self.request.session['user'] = str(user.id)
            redirect(self.request, 'GetUser')
        else:
            self.request.status.update({"err": "Логин и пароль не совпадают"})
            return {}


class AddFollow (web.View):
    async def post(self):
        toward = self.request.data.toward
        user = self.request.user
        try:
            await self.request.app.objects.create(Followers, toward, user.id)
        except:
            self.request.status.update({"err": "Не удалось подписаться"})
        return {}

class EditFollow(web.View):
    async def post(self):
        user = self.request.user
        data = self.request.data
        id = self.request.match_info['id']
        if not data:
            query = Followers.delete().where(Followers.whom == user.id, Followers.toward == id)
            await self.request.app.objects.execute(query)
            return {}

class GetFollowers(web.View):
    async def get(self):
        user = self.request.user
        followers = []
        id = self.request.rel_url.query.get('id', user.id)
        if id == user.id:
            try:
                query = User.select(User).join(Followers, on=(Followers.whom == User.id)).where(
                    Followers.toward == id)
                result = await self.request.app.objects.execute(query)
                for flwr in result:
                    followers.append(flwr.serialize())
                return {"followers": followers}
            except:
                self.request.status.update({"err": "Не удалось получить подписчиков"})
                return {}
        else:
            try:
                query = User.select(User).join(Followers, on=(Followers.whom == User.id)).where(
                    Followers.toward == id)
                result = await self.request.app.objects.execute(query)
                for flwr in result:
                    followers.append(flwr.serialize())
                return {"followers": followers}
            except:
                self.request.status.update({"err": "Не удалось получить подписчиков"})
                return {}

class GetFollows(web.View):
    async def get(self):
        user = self.request.user
        followers = []
        id = self.request.rel_url.query.get('id', user.id)
        if id == user.id:
            try:
                query = User.select(User).join(Followers, on=(Followers.toward == User.id)).where(
                    Followers.whom == id)
                result = await self.request.app.objects.execute(query)
                for flwr in result:
                    followers.append(flwr.serialize())
                return {"followers": followers}
            except:
                self.request.status.update({"err": "Не удалось получить подписчиков"})
                return {}
        else:
            try:
                query = User.select(User).join(Followers, on=(Followers.toward == User.id)).where(
                    Followers.whom == id)
                result = await self.request.app.objects.execute(query)
                for flwr in result:
                    followers.append(flwr.serialize())
                return {"followers": followers}
            except:
                self.request.status.update({"err": "Не удалось получить подписчиков"})
                return {}