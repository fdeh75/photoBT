'''
Created on May 23, 2018

@author: fdeh
'''
import os
ffmpeg = "ffmpeg -f image2 -framerate 2 -pattern_type glob -i '%s' -r 30 -s 1920x1080 %s"

def photoToVideo(path):
#    os.system("cd "+path)
#    os.system("ls")
#    os.system('ffmpeg -i /home/fdeh/Pictures/foto/test_py_ffm/' + chr(34) + '*.JPG'+ chr(34) + ' -f image2 -framerate 6 -s 1920x1080 /home/fdeh/Pictures/foto/test_py_ffm/video.mp4')
    jpegs = ""
    for f in os.listdir(path):
        jpegs = jpegs + " "+ f
    os.system(ffmpeg % (os.path.join(path, '*.JPG'), os.path.join(path,"video.mp4")))
    
if __name__ == '__main__':
    p = "/home/fdeh/Pictures/foto/test_py_ffm"
    print(ffmpeg % (os.path.join(p,"'*.JPG'"), os.path.join(p,"video.mp4")))
    photoToVideo(p)
    pass