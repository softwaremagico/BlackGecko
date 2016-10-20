import logging
import asyncio

from config import ConfigurationReader

class SensorsController():
	_events_initialized = False
	_loop = None

	
	def __init__(self, message_manager_f):
		self._message_manager = message_manager_f
		self.enable_sensors()


	def enable_sensors(self):
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
				self.sensor_started()
		except ImportError:
			logging.error("No GPIO library found! Sensors are not enabled!")
			self.sensor_error(message_manager_f, "🚫 No GPIO library found! Sensors are not enabled! 🚫")


	def on_gpio_motion_event(self, channel):
		print('Motion detected')
		self._loop.call_soon_threadsafe(self.gpio_motion_event_on_loop_thread)


	def on_gpio_sound_event(self, channel):
		print('Sound detected')
		self._loop.call_soon_threadsafe(self.gpio_sound_event_on_loop_thread)


	def gpio_motion_event_on_loop_thread(self):
		asyncio.async(self._message_manager("🚨 Motion detected in '" + ConfigurationReader._alias + "'! 🚨 "))


	def gpio_sound_event_on_loop_thread(self):
		asyncio.async(self._message_manager("🚨 Sound detected in '" + ConfigurationReader._alias + "'!  🚨 "))
	
	
	def sensor_started(self):
		asyncio.async(self._message_manager("Enabling node '" + ConfigurationReader._alias + "' 🏁"))

		
	def sensor_error(self, message):
		asyncio.async(self._message_manager(message))
