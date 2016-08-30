import logging
import asyncio

from config import ConfigurationReader

logging.basicConfig(filename=ConfigurationReader._log_file, level=logging.INFO)

class SensorsController():
	_events_initialized = False

	
	def __init__(self, message_manager_f):
		self.enable_sensors(message_manager_f)


	def enable_sensors(self, message_manager_f):
		try:
			import RPi.GPIO as gpio
			logging.info("Sensors enabled!")
			if self._events_initialized == False :
				self._events_initialized = True
				if ConfigurationReader._infrared_sensor_pin > 0 :
					gpio.add_event_detect(ConfigurationReader._infrared_sensor_pin, gpio.RISING, callback=lambda x: self.motion_sensor(message_manager_f), bouncetime=500)
				if ConfigurationReader._sound_sensor_pin > 0 :
					gpio.add_event_detect(ConfigurationReader._sound_sensor_pin, gpio.RISING, callback=lambda x: self.sound_sensor(message_manager_f), bouncetime=500)
				self.sensor_started(message_manager_f)
		except ImportError:
			logging.error("No GPIO library found! Sensors are not enabled!")
			self.sensor_error(message_manager_f, "🚫 No GPIO library found! Sensors are not enabled! 🚫")
	
			
	def motion_sensor(self, message_manager_f):
		asyncio.async(message_manager_f("🚨 Motion detected in '" + self._alias + "'! 🚨"))


	def sound_sensor(self, message_manager_f):
		asyncio.async(message_manager_f("📢 Sound detected in '" + self.__alias + "'! 📢"))

		
	def sensor_started(self, message_manager_f):
		asyncio.async(message_manager_f("Enabling node '" + self._alias + "' 🏁"))

		
	def sensor_error(self, message_manager_f, message):
		asyncio.async(message_manager_f(message))
