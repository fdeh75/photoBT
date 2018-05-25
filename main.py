#!/usr/bin/python3.6
import asyncio
import os
import serial
import aiohttp.web

import aiohttp_autoreload
import aiohttp_cors

from config.main import config



#import com


def searchCom():
    flag = True
    d = ''
    while flag:
        for devises in os.listdir('/dev/'):
            if 'ttyUSB' in devises:
                try:
                    ser = serial.Serial('/dev/' + devises, 115200)            
                    if 'PULT' in get_com(ser):
                        d = devises
                        flag = False
                except:
                    print('ret')
    #        else:
    #                print("The device could not be connected..\n")
        time.sleep(2)
    print("The device is connected successfully.. ", d, "\n")    
    return 0

templateCap = """
<div style="position:absolute;left:50%;top:50%;margin-left:-100px;margin-top:-50px;text-align:center">
    <p>
    Plese, connect the device..
    </p>
</div>
"""

def prepage_handler(reqvest):
    response = web.Response(body=templateCap.encode(),content_type='text/html')

    return 
def main():
    print("main ok\n")
    loop = asyncio.get_event_loop()
    
    
#    searchCom()
    from handlers.main import page_handler
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
#    try:
    main()
#    except:
#        exit()