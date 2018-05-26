import asyncio
import os

from aiohttp import web

import cloud.cloud
import convert.convert

from capture.capture import get_captures_list, get_camera_list, currentCameras

templateCap = """
<div style="position:absolute;left:50%;top:50%;margin-left:-100px;margin-top:-50px;text-align:center">
    <form method="POST" action="/">
        <input type="submit" value="capture" name="cap">
        <input type="submit" value="setup" name="set">
    </form><br />
</div>
"""
templateVideo = """
<div style="position:absolute;left:50%;top:50%;margin-left:-100px;margin-top:-50px;text-align:center">
    <video controls width="400" height="300">
        <source src="%s" type="video/mp4">
    </video>
    <form method="GET" action="/">
        <input type="submit" value="capture">
    </from><br />
    
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

def caping(dest):
#    dest = '/home/fdeh/Pictures/test'
    tmp = os.listdir(dest)
    for thumb in tmp:
        if 'CAM' in thumb:
            break
    #try:
    cloud.cloud.sendVideo(dest + 'video.mp4',dest + '/' + thumb)
    #except:
 #   print("Files dont uploaded")
    return 0

async def page_handler(request):
    print(dir())
    data = await request.post()
    message = ""
    template = templateCap
    dest = ''
    thumb = ''
    
    if "cap" in data:
        d = get_captures_list(request.app.loop)
        convert.convert.photoToVideo(d)
        caping(d)
        d = d + '/video.mp4'
#        template = templateVideo % d
        
    if "set" in data:
        Cameras = (get_camera_list(request.app.loop))
        template = (templateSetPre + Cameras + templateSetPost)

    response = web.Response(body=template.encode(),content_type='text/html')


    return response


if __name__ == '__main__':
    print(dir(cloud))

