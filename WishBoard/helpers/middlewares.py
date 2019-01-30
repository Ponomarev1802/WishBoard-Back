from aiohttp_session import get_session
from aiohttp import web

from user.models import User


async def request_user_middleware(app, handler):
    async def middleware(request):
        #print ('enter in middleware 1')
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
        request.status.update({"auth": auth})
        #print(response)
        return response
    return middleware


async def json_response(app, handler):
    async def middleware(request):
        #print('enter in middleware 2')
        res = await handler(request)
        print(res)
        return web.json_response(res)
    return middleware


async def request_checker(app, handler):
    async def middleware(request):
        #print('enter in middleware 3')
        if request.method == "POST":
            try:
                request.data = await request.json()
            except:
                request.status.update({"err": "invalid request"})
                return {}
        res = await handler(request)
        return res
    return middleware


async def status_initial(app, handler):
    async def middleware(request):
        #print('enter in middleware 4')
        request.status = {"auth": False, "err": ""}
        res = await handler(request)
        #print(response)
        res.update({"status": request.status})
        return res
    return middleware
