# -*- coding: utf-8 -*-
#Importing the necessary modules
import threading
import serial
import RPi.GPIO as GPIO
import cv2
import numpy as np
import os
from threading import Thread
import time
import urllib2
import urllib

####LOAD####
#Loading OpenCV cascades and activating the pins 
eyeCascade = cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_mcs_eyepair_small.xml")
glassCascade = cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_eye_tree_eyeglasses.xml")
GPIO.setmode(GPIO.BCM)
lstPins = [7,8,25] #De pinnen die gebruikt worden
GPIO.setup(24, GPIO.IN)
for pin in lstPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

#Database connection
#Host
HOST = "http://54.200.177.96"
#Device identifier
DEVICE_KEY = "7d9557d36bb0339b2a021d0d12ec4ee3"
#Sensors
SENSOR_LIGHT = "light"
SENSOR_TEMPERATURE = "temperature"
SENSOR_HUMIDITY = "humidity"
SENSOR_CAMERA = "camera"
SENSOR_SOUND = "sound"

####OPENCV####
#Identifying eyes
def findEyes(eyeCascade, glassCascade):
    img = cv2.imread("photo.jpg")
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eyeCascade.detectMultiScale(grayImg)
    if len(eyes) == 0:
        glasses = glassCascade.detectMultiScale(grayImg)
        if len(glasses) == 0:
            return False
    return True

#Taking a photo           
def takePic():
    os.system("sudo raspistill -o photo.jpg -t 0 -n -w 300 -h 200")

#Controlling the led
def setLedColor(color):
    if color == 'green':
        GPIO.output(8, True)
        GPIO.output(7, False)
        GPIO.output(25, False)
    if color == 'red':
        GPIO.output(8, False)
        GPIO.output(7, True)
        GPIO.output(25, False)
    if color == 'blue':
        GPIO.output(8, False)
        GPIO.output(7, False)
        GPIO.output(25, True)
    if color == "off":
        GPIO.output(8, False)
        GPIO.output(7, False)
        GPIO.output(25, False)   

#Main function for eye identification
def startOpenCVTracking():
    while True:
        takePic()
        global eyeCascade, glassCascade
        result = findEyes(eyeCascade,glassCascade)
        if result == True:
            setLedColor('green')
        else:
            setLedColor('red')
        postSensorData(SENSOR_CAMERA, result)
        
####ARDUINO####  
#Main funtion for retrieving the sensorvalues from the Arduino
def startArduinoTracking():
    arduino = serial.Serial('/dev/serial/by-id/usb-Gravitech_ARDUINO_NANO_13BP0810-if00-port0')
    while True:
        sensorValues = arduino.readline()
        #print sensorValues
        if len(sensorValues) > 0:
            l,h,t,s = splitSensorValues(sensorValues)   #Light, Humidity, Temperature, Sound
            postSensorData(SENSOR_LIGHT, l)
            postSensorData(SENSOR_HUMIDITY, h)
            postSensorData(SENSOR_TEMPERATURE, t)
            postSensorData(SENSOR_SOUND, s)

#Formatting the values
def splitSensorValues(sensorValues):
    l, h, t, s = sensorValues.split("\t")
    if len(l)>3:
        l = l[-3:]
    sound = ""
    for char in s:
        if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
            sound += str(char)
    return l,h,t,sound

###DATABASE###
#Sending a sensorvalue to the database
def postSensorData(sensor, value):
    getRequestParameters = { "deviceKey" : DEVICE_KEY, "sensortype" : sensor, "value" : value, "date" : time.time() }
    response = urllib2.urlopen(HOST + '/sensorData/postSensorData?' + urllib.urlencode(getRequestParameters))
    print response.read()

####THREADS####
#Seperating the work done for the Arduino and the photo-analysis into two threads
#Stand-by for 3 seconds with blue LED to show that the program is ready
setLedColor('blue')
time.sleep(3)
try:
    #THREAD 1: OpenCV
    t1 = Thread(target=startOpenCVTracking, args=())
    t1.daemon = True
    t1.start()
    #THREAD 2: Arduino
    t2 = Thread(target=startArduinoTracking, args=())
    t2.daemon = True
    t2.start()
except:
    print "error"
while 1:
    pass