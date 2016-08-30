import logging
from config import ConfigurationReader

logging.basicConfig(filename=ConfigurationReader._log_file, level=logging.INFO)

class SensorsController():
	_events_initialized = False

	
	def __init__(self, motion_detected_f, sound_detected_f, sensor_started_f, sensor_error_f):
		self.enable_sensors(motion_detected_f, sound_detected_f, sensor_started_f, sensor_error_f)


	def enable_sensors(self, motion_detected_f, sound_detected_f, sensor_started_f, sensor_error_f):
		try:
			import RPi.GPIO as gpio
			logging.info("Sensors enabled!")
			if self._events_initialized == False :
				self._events_initialized = True
				if ConfigurationReader._infrared_sensor_pin > 0 :
					gpio.add_event_detect(ConfigurationReader._infrared_sensor_pin, gpio.RISING, callback=lambda x: motion_detected_f(), bouncetime=500)
				if ConfigurationReader._sound_sensor_pin > 0 :
					gpio.add_event_detect(ConfigurationReader._sound_sensor_pin, gpio.RISING, callback=lambda x: sound_detected_f(), bouncetime=500)
				sensor_started_f()
		except ImportError:
			logging.error("No GPIO library found! Sensors are not enabled!")
			sensor_error_f("No GPIO library found! Sensors are not enabled!")
