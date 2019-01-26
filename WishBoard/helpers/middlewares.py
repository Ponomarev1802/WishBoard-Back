from aiohttp_session import get_session
from aiohttp import web

from user.models import User


async def request_user_middleware(app, handler):
    async def middleware(request):
        request.session = await get_session(request)
        request.user = None
        user_id = request.session.get('user')
        auth = False
        if user_id is not None:
            try:
                request.user = await request.app.objects.get(User, id=user_id)
                auth = True
            except:
                pass
        response = await handler(request)
        response['status'].update({"auth": auth})
        return response
    return middleware

async def json_response(app, handler):
    async def middleware(request):
        res = await handler(request)
        #print(res)
        return web.json_response(res)
    return middleware
