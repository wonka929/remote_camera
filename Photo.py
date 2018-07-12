#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from datetime import datetime
import os
import json
import ftplib


with open('Config_device.json', 'r') as f:
	config = json.load(f)
	for elem in config:
		locals()['{0}'.format(elem)]=config[elem]

CODE= COMMITTENTE + '_' + CPUID


def PiCameraFilter(camera):
	print('Setting camera filter')
	camera.brightness = CAM_brightness #0>freddo 100>caldo
	camera.sharpness = CAM_sharpness #0>freddo 100>caldo
	camera.contrast = CAM_contrast
	camera.saturation = CAM_saturation
	camera.ISO = CAM_ISO
	camera.video_stabilization = CAM_video_stabilization
	camera.exposure_compensation = CAM_exposure_compensation
	camera.exposure_mode = CAM_exposure_mode
	camera.meter_mode = CAM_meter_mode
	camera.awb_mode = CAM_awb_mode
	camera.image_effect = CAM_image_effect
	camera.color_effects = CAM_color_effects
	camera.rotation = CAM_rotation
	camera.hflip = CAM_hflip
	camera.vflip = CAM_vflip
	camera.resolution = (CAM_resolution[0], CAM_resolution[1])
	return camera

def TakePhoto(CODE,directory):
	camera = PiCamera()
	camera = PiCameraFilter(camera)
	filename = datetime.now().strftime("%Y%m%d%H%M_" + CODE + ".jpg")
	print('Taking foto '+ str(filename))
	camera.capture(directory+ '/'+filename)
	camera.close()


# def Clean(SendDirectory):
	# for elem in os.listdir(SendDirectory):
		# if (str(elem.split('_')[0])[:8]) <> (datetime.now().strftime("%Y%m%d")):
			# os.remove(SendDirectory+'/'+elem)


def SendFTP(directory,SendDirectory):
   for filename in os.listdir(directory):
	   print('Sending image:\n'+directory)
	   session = ftplib.FTP('104.40.239.18','waterberry','waterberry_ftp_vm')
	   immagine = open(directory+'/'+filename,'rb')
	   print(directory+'/'+filename)
	   session.storbinary('STOR '+ filename, immagine)
	   print('STOR '+ filename)
	   immagine.close()
	   session.quit()
	   print('Immagine inviata...')
	   os.rename(directory + '/' + filename,SendDirectory + '/' + filename)
	   print('Image moved to sent folder')

	
print('Starting')
directory= '/data/Nuove_Foto'
SendDirectory = '/data/Foto_Inviate'
# Clean(SendDirectory)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)


GPIO.output(21,GPIO.HIGH)
GPIO.output(18,GPIO.HIGH)
print('Flash on')
TakePhoto(CODE,directory)
print('acquiring image')
time.sleep(1)
print('Flash off')
GPIO.output(21,GPIO.LOW)
GPIO.output(18,GPIO.LOW)
SendFTP(directory,SendDirectory)
