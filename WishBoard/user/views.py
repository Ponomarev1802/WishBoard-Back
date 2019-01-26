from aiohttp import web
from .models import User, Wish
from helpers.tools import redirect

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
        #print(wishes)
        return {"user": user.serialize(), "wishes": wishes, "status": {"req": True}}


class addWish(web.View):
    async def post(self):
        wish = await self.request.json()
        try:
            data = await self.request.app.objects.create(Wish, **wish, user=self.request.user)
        except:
            return web.json_response({})
        return web.json_response(data.serialize())

class delWish (web.View):
    async def post(self):
        wish = await self.request.json()
        try:
            wish = await self.request.app.objects.delete(Wish, **wish, user=self.request.user)
            print(wish)
        except:
            print('not deleted')

class newUser(web.View):
    async def post(self):
        data = await self.request.json()
        #print(data)
        try:
            user = await self.request.app.objects.create(User, **data)
            return {"status": {"req": True}}
        except:
            return {"status": {"req": False}}



class loginUser(web.View):
    async def post(self):
        data = await self.request.json()
        #print (data)
        try:
            user = await self.request.app.objects.get(User, **data)
        except:
            return {"status": {"req": False}}
        if user:
            self.request.session['user'] = str(user.id)
            redirect(self.request, 'getUser')
        return {"status": {"req": False}}