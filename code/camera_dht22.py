#!/usr/bin/python3
# -*- coding: utf-8 -*-
from picamera import PiCamera
import time
from time import sleep
from twython import Twython
from datetime import datetime
import Adafruit_DHT

sensor_aussen = Adafruit_DHT.DHT22
pin_aussen = 20

camera = PiCamera()
camera.rotation = 180
#camera.start_preview()
sleep(5)
camera.capture('/home/pi/image.jpg')
#camera.stop_preview()

from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

while 1:
        humidity_aussen, temperature_aussen = Adafruit_DHT.read_retry(sensor_aussen, pin_aussen)
        if humidity_aussen is not None and temperature_aussen is not None:

           message = "#Wetter"
           message  += " am: %s - " %datetime.now ().strftime ('%d.%m.%Y um %H:%M Uhr')
           message  += "Temp: %0.1f°C" % (temperature_aussen)
           message  += " Luftfeuchte: %0.1f%%" % (humidity_aussen)
           message  += " #scoutlab #frankenthal"
           time.sleep(600)
           with open('/home/pi/image.jpg', 'rb') as photo:
            response = twitter.upload_media(media=photo)
           twitter.update_status(status=message, media_ids=[response['media_id']])
           print("Tweeted: %s" % message)

        else:
                        print('Fehler beim Einlesen der Daten. Starte einen weiteren Versuch!')
