from aiohttp import web
from .models import User, Wish
import aiohttp_jinja2
from helpers.tools import redirect
import json
from playhouse.shortcuts import model_to_dict

from helpers.decorators import anonymous_required, login_required


class getUser(web.View):
    @login_required
    async def get(self):
        user = self.request.user
        wishes = []
        try:
            query = await self.request.app.objects.execute(user.wishes)
            for wish in query:
                wishes.append(wish.serialize())
        except:
            pass
        return {"user": user.serialize(), "wishes": wishes}

class addWish(web.View):
    async def post(self):
        wish = await self.request.json()
        try:
            data = await self.request.app.objects.create(Wish, **wish, user=self.request.user)
        except:
            return web.json_response({})
        return web.json_response(data.serialize())

class newUser(web.View):
    @aiohttp_jinja2.template('accounts/register.html')
    async def get(self):
        return{}

    async def post(self):
        data = await self.request.post()
        user = await self.request.app.objects.create(User, **data)
        return web.json_response(user.serialize())



class loginUser(web.View):

    @aiohttp_jinja2.template('accounts/login.html')
    async def get(self):
        return{}

    async def post(self):
        data = await self.request.json()
        try:
            user = await self.request.app.objects.get(User, **data)
        except:
            return web.json_response({})
        if user:
            self.request.session['user'] = str(user.id)
        return redirect(self.request, 'getUser')