from config import ConfigurationReader

class SensorsController():
	_events_initialized = False

	
	def __init__(self, motion_detected_f, sound_detected_f):
		self.enable_sensors(motion_detected_f, sound_detected_f)


	def enable_sensors(self, motion_detected_f, sound_detected_f):
		try:
			import RPi.GPIO as gpio
			print("Sensors enabled!")
			if self._events_initialized == False :
				self._events_initialized = True
				if ConfigurationReader._infrared_sensor_pin > 0 :
					gpio.add_event_detect(ConfigurationReader._infrared_sensor_pin, gpio.RISING, callback=lambda x: motion_detected_f(), bouncetime=500)
				if ConfigurationReader._sound_sensor_pin > 0 :
					gpio.add_event_detect(ConfigurationReader._sound_sensor_pin, gpio.RISING, callback=lambda x: sound_detected_f(), bouncetime=500)
		except ImportError:
			print("No GPIO library found! Sensors are not enabled!")
