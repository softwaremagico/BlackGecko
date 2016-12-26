import logging
import asyncio

from config import ConfigurationReader

class SensorsController():
	_events_initialized = False
	_loop = None
	_sensors_started = False

	
	def __init__(self, message_manager_f, detection_callback):
		self._message_manager = message_manager_f
		self.initialize_sensors()
		self._detection_callback = detection_callback

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
					gpio.add_event_detect(ConfigurationReader._sound_sensor_pin, gpio.RISING, callback=self.on_gpio_sound_event, bouncetime=500)
				logging.info("Sensors enabled!")
				# run the event loop
				self._loop = asyncio.get_event_loop()
		except ImportError:
			logging.error("No GPIO library found! Sensors are not enabled!")
			self.sensor_error(message_manager_f, "🚫 No GPIO library found! Sensors are not enabled! 🚫")


	def on_gpio_motion_event(self, channel):
		self._loop.call_soon_threadsafe(self.gpio_motion_event_on_loop_thread)


	def on_gpio_sound_event(self, channel):
		self._loop.call_soon_threadsafe(self.gpio_sound_event_on_loop_thread)


	def gpio_motion_event_on_loop_thread(self):
		if self._sensors_started :
			logging.info("Motion detected!")
			asyncio.async(self._message_manager("🚨 Motion detected in '" + ConfigurationReader._alias + "'! 🚨 "))
			self._detection_callback()


	def gpio_sound_event_on_loop_thread(self):
		if self._sensors_started :
			logging.info("Sound detected!")
			asyncio.async(self._message_manager("🚨 Sound detected in '" + ConfigurationReader._alias + "'!  🚨 "))
	
	
	def sensor_started(self):
		asyncio.async(self._message_manager("Sensors in '" + ConfigurationReader._alias + "' enabled  🏁"))

	def sensors_disabled(self):
		asyncio.async(self._message_manager("Sensors in '" + ConfigurationReader._alias + "' disabled 🚫"))
		
	def sensor_error(self, message):
		asyncio.async(self._message_manager(message))

	def enable_sensors(self):
		if self._events_initialized == False :
			self.initialize_sensors()			
		self.sensor_started()
		self._sensors_started = True

	def disable_sensors(self):
		self._sensors_started = False
		self.sensors_disabled()
