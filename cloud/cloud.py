from YaDiskClient.YaDiskClient import YaDisk

from InstagramAPI import InstagramAPI


foo = '/home/fdeh/Videos/Landscape.mp4'
img = '/home/fdeh/Pictures/panda.jpg'
videoPath = "/video-bt"
insta_user,insta_psw = '',''
yadisk_user,yadisk_psw = '',''
logins = open('./accounts.txt', 'r')
for line in logins:
    line = line.split(' ')
    line[1] = line[1].strip("\n").strip(' ')
    if 'insta_user' in line:
        insta_user = line[1]
    if 'insta_psw' in line:
        insta_psw = line[1]        
    if 'yadisk_user' in line:
        yadisk_user = line[1] 
    if 'yadisk_psw' in line:
        yadisk_psw = line[1]  
logins.close()

InstagramAPI = InstagramAPI(insta_user,insta_psw)
InstagramAPI.login()
disk = YaDisk(yadisk_user,yadisk_psw)


def sendVideo(videoFile, thumb):
    InstagramAPI.uploadVideo(videoFile,thumb, caption="Tortuguero")
    try:
        disk.ls(videoPath)
    except:
        print('exc')
        disk.mkdir(videoPath)
        print('video-bt created')
    i = 0
    while True:
        if "video" + str(i) + ".mp4" in str(disk.ls(videoPath)):
            print('video', "video" + str(i) + ".mp4", 'detekt') 
        else:
            disk.upload(videoFile, "/video-bt" + "/video" + str(i) + ".mp4")
            break
        i = i + 1
    print('Uploding done')
    return 0

if __name__ == '__main__':
#    try: ADD -r 30 and copipasre video
    InstagramAPI.uploadVideo('/home/fdeh/workspase/photoBT/photos/2018_05_23_part:6/video5.mp4','/home/fdeh/workspase/photoBT/photos/2018_05_23_part:6/CAM_13_IMG_9488.JPG', caption="Tortuguero")
#    InstagramAPI.uploadVideo('/home/fdeh/Videos/Landscape.mp4','/home/fdeh/workspase/photoBT/photos/2018_05_23_part:6/CAM_13_IMG_9488.JPG', caption="Tortuguero")
    
    
    
    