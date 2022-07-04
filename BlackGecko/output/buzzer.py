import logging
import asyncio
import time

from config import ConfigurationReader

class Buzzer():

	def __init__(self):
		if int(ConfigurationReader._buzzer_pin) > 0 :
			asyncio.ensure_future(self.alarm())


	@asyncio.coroutine
	def alarm(self):
		try:
			import RPi.GPIO as GPIO
			logging.info("Alarm started!")
			GPIO.setmode(GPIO.BCM)
			GPIO.setwarnings(False)
			GPIO.setup(ConfigurationReader._buzzer_pin, GPIO.OUT)
			iteration = 0
			sound = True
			while iteration < 10:
			        GPIO.output(ConfigurationReader._buzzer_pin, sound) 
		        	time.sleep(1)
			        sound = not sound
			        iteration = iteration + 1

			#GPIO.cleanup()
			logging.info("Alarm stopped!")
		except ImportError:
			logging.error("No GPIO library found! Alarm is not enabled!")


