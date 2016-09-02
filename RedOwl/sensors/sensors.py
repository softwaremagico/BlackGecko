import logging
import asyncio

from config import ConfigurationReader

class SensorsController():
	_events_initialized = False

	
	def __init__(self, message_manager_f):
		self.enable_sensors(message_manager_f)


	def enable_sensors(self, message_manager_f):
		try:
			import RPi.GPIO as gpio
			if self._events_initialized == False :
				self._events_initialized = True
				#Define raspberry gpio input/output
				gpio.setmode(gpio.BCM)
				if int(ConfigurationReader._infrared_sensor_pin) > 0 :
					gpio.setup(ConfigurationReader._infrared_sensor_pin, gpio.IN)
					gpio.add_event_detect(ConfigurationReader._infrared_sensor_pin, gpio.RISING, callback=lambda x: self.motion_sensor(message_manager_f), bouncetime=500)
				if ConfigurationReader._sound_sensor_pin > 0 :
					gpio.setup(ConfigurationReader._sound_sensor_pin, gpio.IN)
					gpio.add_event_detect(ConfigurationReader._sound_sensor_pin, gpio.RISING, callback=lambda x: self.sound_sensor(message_manager_f), bouncetime=500)
				logging.info("Sensors enabled!")
				self.sensor_started(message_manager_f)
		except ImportError:
			logging.error("No GPIO library found! Sensors are not enabled!")
			self.sensor_error(message_manager_f, "🚫 No GPIO library found! Sensors are not enabled! 🚫")
	
			
	def motion_sensor(self, message_manager_f):
		asyncio.async(message_manager_f("🚨 Motion detected in '" + ConfigurationReader._alias + "'! 🚨"))


	def sound_sensor(self, message_manager_f):
		asyncio.async(message_manager_f("📢 Sound detected in '" + ConfigurationReader.__alias + "'! 📢"))

		
	def sensor_started(self, message_manager_f):
		asyncio.async(message_manager_f("Enabling node '" + ConfigurationReader._alias + "' 🏁"))

		
	def sensor_error(self, message_manager_f, message):
		asyncio.async(message_manager_f(message))
