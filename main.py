#!/usr/bin/python3.6
import asyncio
import os

import aiohttp.web

import aiohttp_autoreload
import aiohttp_cors

from config.main import config

from handlers.main import page_handler



def main():
    print("main ok\n")
    loop = asyncio.get_event_loop()
    app = aiohttp.web.Application(loop=loop)

    app.router.add_route("*", "/", page_handler)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    for route in list(app.router.routes()):
        if route._method != '*':
            cors.add(route, {"*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                allow_headers="*",
            )})

    aiohttp_autoreload.start()

    aiohttp.web.run_app(app, host=config['host'], port=config['port'])


if __name__ == '__main__':
    try:
        main()
    except:
        exit()