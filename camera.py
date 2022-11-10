#!/usr/bin/python

#Credit: https://github.com/mistylackie/raspberry-pi-camera-to-aws-s3/blob/master/camera.py

from picamera import PiCamera
from time import sleep
import datetime as dt
import sys
import subprocess
import os

from dotenv import dotenv_values
env_var = dotenv_values(".env")

BUCKET = env_var["S3_BUCKET"]
SRC_DIR = "/home/pi/Desktop/images/"
DEST = BUCKET + "upload"
CURRENT_DATE = dt.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
IMAGE_NAME = dt.datetime.now().strftime('%m%d%Y%H%M%S')

camera = PiCamera()

camera.resolution = (600, 600)
camera.framerate = 15
camera.start_preview()
camera.annotate_text = CURRENT_DATE

sleep(10)
camera.capture('/home/pi/Desktop/images/'+IMAGE_NAME+'.jpg')
camera.stop_preview()

CMD = "s3cmd put --acl-public %s/*.* %s" % (SRC_DIR, DEST)
subprocess.call(CMD, shell=True)

os.remove('/home/pi/Desktop/images/'+IMAGE_NAME+'.jpg')
