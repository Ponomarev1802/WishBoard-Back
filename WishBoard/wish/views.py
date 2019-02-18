from aiohttp import web
from .models import Wish


class AddWish(web.View):
    async def post(self):
        wish = self.request.data
        try:
            res = await self.request.app.objects.create(Wish, **wish, user=self.request.user)
            print(res)
        except:
            self.request.status.update({"err": "не удалось записать Wish в базу"})
        return {}


class EditWish (web.View):
    async def post(self):
        wish_id = self.request.match_info['id']
        wish = self.request.data
        if wish:
            try:
                query = (Wish.update(**wish).where(Wish.id == wish_id))
                await self.request.app.objects.execute(query)
            except:
                self.request.status.update({"err": "Не удалось обновить wish"})
        else:
            try:
                query = Wish.delete().where(Wish.id == wish_id, Wish.user_id == self.request.user.id)
                await self.request.app.objects.execute(query)
            except:
                self.request.status.update({"err": "невозможно удалить Wish"})
        return {}


class GetWish(web.View):
    async def get(self):
        user = self.request.user
        id = self.request.rel_url.query.get('user', user.id)
        wishes = []
        if id == user.id:
            try:
                query = await self.request.app.objects.execute(user.wishes)
                for wish in query:
                    wishes.append(wish.serialize())
            except:
                pass
        return {"wishes": wishes}

class GetWishFull(web.View):
    async def get(self):
        user = self.request.user
        wish_id = self.request.match_info['id']
        wish_query = await self.request.app.objects.get(Wish(wish_id))
        wish = wish_query
        comments = []
        excludes = []
        try:
            comments_query = await self.request.app.objects.execute(wish.comments)
            for comment in comments_query:
                comments.append(comment.serialize())
        except:
            pass
        try:
            excludes_query = await self.request.app.objects.execute(wish.exclude)
            for exlude in excludes_query:
                excludes.append(exlude.serialize())
        except:
            pass
        wish = wish.serialize()
        wish.update({'comments': comments})
        wish.update({'excludes': excludes})
        return wish
