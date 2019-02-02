# Not real migrations, just create tables

from user.models import User
from wish.models import Wish

from aiohttp import web


class Migrate(web.View):
    def get(self):
        self.request.app.database.set_allow_sync(True)
        User.create_table(True)
        Wish.create_table(True)
        return {"status": "success"}