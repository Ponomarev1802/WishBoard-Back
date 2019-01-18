from aiohttp_session import get_session

from user.models import User


async def request_user_middleware(app, handler):
    async def middleware(request):
        request.session = await get_session(request)
        request.user = None
        user_id = request.session.get('user')
        if user_id is not None:
            try:
                request.user = await request.app.objects.get(User, id=user_id)
            except:
                pass
        return await handler(request)
    return middleware