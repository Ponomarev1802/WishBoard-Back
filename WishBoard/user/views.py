from aiohttp import web
from .models import User, Wish
from helpers.tools import redirect

from helpers.decorators import login_required


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
        #print(wishes)
        return {"user": user.serialize(), "wishes": wishes, "status": {"req": True}}


class addWish(web.View):
    async def post(self):
        wish = self.request.data
        try:
            data = await self.request.app.objects.create(Wish, **wish, user=self.request.user)
        except:
            self.request.update({"err": "не удалось записать Wish в базу"})
        return {}

class delWish (web.View):
    async def post(self):
        wish = self.request.data
        #print(wish)
        try:
            query = Wish.delete().where(Wish.id == wish['id'], Wish.user_id == self.request.user.id)
            wish = await self.request.app.objects.execute(query)
        except:
            self.request.status.update({"err": "cant delete"})
        return {}

class newUser(web.View):
    async def post(self):
        data = self.request.data
        #print(data)
        try:
            user = await self.request.app.objects.create(User, **data)
        except:
            self.request.status.update({"req": False})
        return {}



class loginUser(web.View):
    async def post(self):
        data = self.request.data
        #print (data)
        try:
            user = await self.request.app.objects.get(User, **data)
        except:
            self.request.status.update({"req": False})
        if user:
            self.request.session['user'] = str(user.id)
            redirect(self.request, 'getUser')
        self.request.status.update({"req": False})
        return {}