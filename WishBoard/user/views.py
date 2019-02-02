from aiohttp import web
from .models import User
from helpers.tools import redirect

from helpers.decorators import login_required


class GetUser(web.View):
    @login_required
    async def get(self):
        user = self.request.user
        id = self.request.GET.get('id', user.id)
        if id == user.id:
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



class loginUser(web.View):
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