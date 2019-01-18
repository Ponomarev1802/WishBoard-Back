# Not real migrations, just create tables

from user.models import User, Wish

from aiohttp import web


class Migrate(web.View):
    def get(self):
        self.request.app.database.set_allow_sync(True)
        User.create_table(True)
        Wish.create_table(True)
        return web.Response(text='all tables is created')



#    for room in ('main', 'flood', 'foo', 'bar', 'baz', ):
#        try:
#            Room.create(name=room)
#       except:
#            pass
#
#    for user in ('Alice', 'Bob', 'Carol', 'Dave', 'Eve', ):
#        try:
#            User.create(username=user)
#        except:
#            pass
