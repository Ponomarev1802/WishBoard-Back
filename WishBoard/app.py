import asyncio
import aioredis
import jinja2
import peewee_async

import aiohttp_jinja2

from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.redis_storage import RedisStorage

import settings
from routes import setup_routes

from settings import logger
from helpers.middlewares import request_user_middleware,json_response, request_checker,status_initial
from helpers.template_tags import tags
from helpers.models import database


async def create_app(loop):
    """ Prepare application """
    redis_pool = await aioredis.create_pool(settings.REDIS_CON, loop=loop)
    middlewares = [session_middleware(RedisStorage(redis_pool)), json_response, status_initial, request_checker, request_user_middleware]
    # init application
    app = web.Application(loop=loop, middlewares=middlewares)
    app.redis_pool = redis_pool
    app.wslist = {}
    jinja_env = aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIR),
        context_processors=[aiohttp_jinja2.request_processor], )
    jinja_env.globals.update(tags)
    # db conn
    database.init(**settings.DATABASE)
    app.database = database
    app.database.set_allow_sync(False)
    app.objects = peewee_async.Manager(app.database)
    app.database.connect()

    # make routes
    setup_routes(app)
    app.router.add_static('/static', settings.STATIC_DIR, name='static')

    app.logger = logger
    handler = app.make_handler(access_log=logger)

    serv_generator = loop.create_server(handler, settings.HOST, settings.PORT)
    return serv_generator, handler, app


async def shutdown(server, app, handler):
    """ Safe close server """
    for room in app.wslist.values():
        for peer in room.values():
            peer.send_json({'text': 'Server shutdown'})
    server.close()
    await server.wait_closed()
    app.redis_pool.close()
    await app.redis_pool.wait_closed()
    await app.objects.close()
    await app.shutdown()
    await handler.finish_connections(10.0)
    await app.cleanup()


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    serv_generator, handler, app = loop.run_until_complete(create_app(loop))
    server = loop.run_until_complete(serv_generator)

    logger.debug('Start server '+str(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.debug('Keyboard Interrupt ^C')
    finally:
        logger.debug('Stop server begin')
        loop.run_until_complete(shutdown(server, app, handler))
        loop.close()
    logger.debug('Stop server end')
