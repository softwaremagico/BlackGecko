import logging
import asyncio

from config import ConfigurationReader

class SensorsController():
	_events_initialized = False
	_loop = None

	
	def __init__(self, message_manager_f, motion_detection_callback, sound_detection_callback):
		self._message_manager = message_manager_f
		self.initialize_sensors()
		self._motion_detection_callback = motion_detection_callback
		self._sound_detection_callback = sound_detection_callback

	def initialize_sensors(self):
		try:
			import RPi.GPIO as gpio
			if self._events_initialized == False :
				self._events_initialized = True
				#Define raspberry gpio input/output
				gpio.setmode(gpio.BCM)
				if int(ConfigurationReader._infrared_sensor_pin) > 0 :
					gpio.setup(ConfigurationReader._infrared_sensor_pin, gpio.IN)
					gpio.add_event_detect(ConfigurationReader._infrared_sensor_pin, gpio.RISING, callback=self.on_gpio_motion_event, bouncetime=500)
				if int(ConfigurationReader._sound_sensor_pin) > 0 :
					gpio.setup(ConfigurationReader._sound_sensor_pin, gpio.IN)
					gpio.add_event_detect(ConfigurationReader._sound_sensor_pin, gpio.RISING, callback=self.on_gpio_sound_event, bouncetime=100)
				logging.info("Sensors enabled!")
				# run the event loop
				self._loop = asyncio.get_event_loop()
		except ImportError:
			logging.error("No GPIO library found! Sensors are not enabled!")
			self.sensor_error(message_manager_f, "🚫 No GPIO library found! Sensors are not enabled! 🚫")


	def on_gpio_motion_event(self, channel):
		logging.debug("Motion detected!")
		self._loop.call_soon_threadsafe(self.gpio_motion_event_on_loop_thread)


	def on_gpio_sound_event(self, channel):
		logging.debug("Sound detected!")
		self._loop.call_soon_threadsafe(self.gpio_sound_event_on_loop_thread)


	def gpio_motion_event_on_loop_thread(self):
		self._motion_detection_callback()


	def gpio_sound_event_on_loop_thread(self):
		self._sound_detection_callback()	
	
	def sensor_error(self, message):
		asyncio.ensure_future(self._message_manager(message))

