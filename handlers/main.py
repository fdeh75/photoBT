import asyncio

from aiohttp import web

from capture.capture import get_captures_list, get_camera_list, currentCameras

templateCap = """
<div style="position:absolute;left:50%;top:50%;margin-left:-100px;margin-top:-50px;text-align:center">
    <form method="POST" action="/">
        <input type="submit" value="capture" name="cap">
        <input type="submit" value="setup" name="set">
    </form><br />
</div>
"""
templateSetPre = """
 <div style="position:absolute;left:50%;top:50%;margin-left:-100px;margin-top:-50px;text-align:center">

"""
templateSetPost = """
        <form method="POST" action="/">
        <input type="submit" value="add" name="set">
        <input type="submit" value="done" name="">
    </form><br />
</div>
"""

async def page_handler(request):
    print(dir())
    data = await request.post()
    message = ""
    template = templateCap

    if "cap" in data:
        get_captures_list(request.app.loop)
    if "set" in data:
        Cameras = (get_camera_list(request.app.loop))
        template = (templateSetPre + Cameras + templateSetPost)

    response = web.Response(body=template.encode(),content_type='text/html')


    return response
