#!/usr/bin/python3.6

from __future__ import print_function
from datetime import datetime

import logging
import os
import subprocess
import sys
import io

import asyncio

import subprocess

import time

import com
from testingmf import capt
import lmdb

import gphoto2 as gp


currentCameras = []

def get_serialNumber(cam):
    serialtext = cam.get_summary().text
    splitter = serialtext.splitlines()
    matching = [s for s in splitter if "Serial" in s]
    SNStr = matching[0].split(":")[1].strip()
    return  SNStr

def get_camera_list(loop):
    com.usb_on()
    env = lmdb.open('./cameras_SN.lmdb', max_dbs=10)
    serialNumber_db = env.open_db('serialNumber'.encode())

    logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.ERROR)
    gp.check_result(gp.use_python_logging())
    camera_list = []
    camerasName = ""
    for name, addr in gp.check_result(gp.gp_camera_autodetect()):
        camera = gp.Camera()
        port_info_list = gp.PortInfoList()
        port_info_list.load()
        idx = port_info_list.lookup_path(addr)
        camera.set_port_info(port_info_list[idx])
        camera.init()
        serialStr = get_serialNumber(camera)
        print(serialStr)
        with env.begin(db=serialNumber_db, write=True) as txn:
            if txn.get(serialStr.encode()):
                camerasName = (camerasName + "<p>camera " + txn.get(serialStr.encode()).decode("utf-8") + " dected</p>")
            else:
                if not txn.get('count'.encode()):
                    txn.put('count'.encode(), '1'.encode())
                cameraName = "CAM_" + str(int(txn.get('count'.encode())))
                txn.put('count'.encode(), str(int(txn.get('count'.encode())) + 1).encode())
                txn.put(serialStr.encode(), cameraName.encode())
                camerasName = (camerasName +"<p>camera " + txn.get(serialStr.encode()).decode("utf-8") + " added</p>")
                print("new camera captured")

#    if not camera_list:
#        print('No camera detected')
#        return "none"
    print(camerasName)
    env.close()
    return camerasName


def list_camera_files(camera, path='/'):
    result = []
    # get files
    gp_list = gp.check_result(
        gp.gp_camera_folder_list_files(camera, path))
    for name, value in gp_list:
        result.append(os.path.join(path, name))
    # read folders
    folders = []
    gp_list = gp.check_result(
        gp.gp_camera_folder_list_folders(camera, path))
    for name, value in gp_list:
        folders.append(name)
    # recurse over subfolders
    for name in folders:
        result.extend(list_camera_files(camera, os.path.join(path, name)))
    return result

PHOTO_DIR = './photos'

def list_computer_files():
    result = []
    for root, dirs, files in os.walk(os.path.expanduser(PHOTO_DIR)):
        for name in files:
            if '.thumbs' in dirs:
                dirs.remove('.thumbs')
            if name in ('.directory',):
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext in ('.db',):
                continue
            result.append(os.path.join(root, name))
    return result

def get_target_dir(timestamp):
    dirNameTemp = timestamp.strftime('%Y_%m_%d')
    dirName = dirNameTemp  + '_part:0'
    count = 0
    dirNames = os.listdir(PHOTO_DIR)
    print("dirNames:  ",dirNames)
    print('dirName: ', dirName)
    while dirName in dirNames:
        count = count + 1
        dirName = dirNameTemp + '_part:' + str(count)
    print('Created new dir: ',dirName)
    dirName = dirName + '/'
    return os.path.join(PHOTO_DIR, dirName)

def get_camera_file_info(camera, path):
    folder, name = os.path.split(path)
    return gp.check_result(gp.gp_camera_file_get_info(camera, folder, name))

def get_captures_list(loop):

    current_milli_time = int(round(time.time() * 1000))
    print("CAPTURE BEGIN")

    com.usb_off()
    com.focus_on()
    time.sleep(8)
    com.shot()
    com.focus_off()
    com.usb_on()
    time.sleep(3)

    env = lmdb.open('./cameras_SN.lmdb', max_dbs=10)
    serialNumber_db = env.open_db('serialNumber'.encode())

    logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.ERROR)
    gp.check_result(gp.use_python_logging())
    timestamp = datetime.now()
    dest_dir = get_target_dir(timestamp)
    for name, addr in gp.check_result(gp.gp_camera_autodetect()):
        time0 = int(round(time.time() * 1000))
        camera = gp.Camera()
        port_info_list = gp.PortInfoList()
        port_info_list.load()
        idx = port_info_list.lookup_path(addr)
        camera.set_port_info(port_info_list[idx])
        camera.init()
        computer_files = list_computer_files()
        serialStr = get_serialNumber(camera)
        with env.begin(db=serialNumber_db) as txn:

            cameraName = txn.get(serialStr.encode()).decode("utf-8")
            print('Capturing image', cameraName)
            camera_files = list_camera_files(camera)
            if not camera_files:
                print('No files found')
                return 1
            print('Copying files...')
            for path in camera_files:
                info = get_camera_file_info(camera, path)
#                timestamp = datetime.fromtimestamp(info.file.mtime)
                folder, name = os.path.split(path)
                dest = os.path.join(dest_dir, cameraName + '_' + name )
                if dest in computer_files:
                    continue
                print('%s -> %s' % (path, dest_dir + cameraName + '_' + name))
                if not os.path.isdir(dest_dir):
                    os.makedirs(dest_dir)
                camera_file = gp.check_result(gp.gp_camera_file_get(
                    camera, folder, name, gp.GP_FILE_TYPE_NORMAL))
                gp.check_result(gp.gp_file_save(camera_file, dest))
                gp.check_result(gp.gp_camera_file_delete(camera, folder, name))
                time1 = int(round(time.time() * 1000))
                time_f = time1 - time0
                print(cameraName,' cap time (mS): ', time_f)
#            env.close()
        gp.check_result(gp.gp_camera_exit(camera))
    com.usb_off()
    current_milli_time1 = int(round(time.time() * 1000))
    time_f = current_milli_time1-current_milli_time
    print('all time (mS): ',time_f)

        #    with env.begin() as txn:
#        for key, value in txn.cursor(db=serialNumber_db):
#            print('  ', key, value, "/n")
#            current_config.append({key,value})
#    print("C_C: ",current_config)



                                 #debug


    #
    # com.usb_on()                                    #debug
    # time.sleep(3)
    # com.usb_off()
    # camera_list.sort(key=lambda x: x[0])
    # print(camera_list)
    # com.usb_off()
    #
    # camera_list = []
    # for name, addr in gp.check_result(gp.gp_camera_autodetect()):
    #     camera_list.append((name, addr))
    # if not camera_list:
    #     print('No camera detected')
    #     return 1
    # camera_list.sort(key=lambda x: x[0])
    # # ask user to choose one
    # tasks = []
    # for camera_item in camera_list:
    #     name, addr = camera_item
    #     print(f"{name} {addr}")
    #     camera = gp.Camera()
    #
    #     # search ports for camera port name
    #     port_info_list = gp.PortInfoList()
    #     port_info_list.load()
    #     idx = port_info_list.lookup_path(addr)
    #     camera.set_port_info(port_info_list[idx])
    #     camera.init()
    #
    #     tasks.append(asyncio.ensure_future(set_capture(camera)))
    #
    # asyncio.gather(*tasks, loop=loop)
    cmds = ['/usr/local/bin/ffprobe', '-f image2', '-pattern_type glob','-framerate 6','-i ./photo/*.JPG',' -s 1920x1080', './photo/video.mp4']
    return dest_dir

async def set_capture(camera):


    print('Capturing image')
    file_path = gp.check_result(gp.gp_camera_capture(
        camera, gp.GP_CAPTURE_IMAGE))
    #
    print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
    # target = os.path.join('/server/VIDAVISI/photo/photos', f"{addr}_{file_path.name}")
    # print('Copying image to', target)
    # camera_file = gp.check_result(gp.gp_camera_file_get(
    #     camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
    # gp.check_result(gp.gp_file_save(camera_file, target))
