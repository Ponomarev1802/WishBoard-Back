from aiohttp import web
from helpers.tools import redirect, add_message


def json_response(func):
    """ Wrapper for view method, to return JsonResponse """
    async def wrapped(*args, **kwargs):
        content, status = await func(*args, **kwargs)
        return web.json_response(data=content, status=status)
    return wrapped


def login_required(func):
    """ Отказ в доступе для неавторизованных пользователей """
    async def wrapped(self, *args, **kwargs):
        if self.request.user is None:
            self.request.status.update({"err": "forbidden"})
            return {}
        return await func(self, *args, **kwargs)
    return wrapped


def anonymous_required(func):
    """ Отказ в доступе для авторизованных пользователей """
    async def wrapped(self, *args, **kwargs):
        if self.request.user is not None:
            return {"status": {"err": "you're already logged in"}}
        return await func(self, *args, **kwargs)
    return wrapped
