import logging

from config import ConfigurationReader

red_led_pwm = None
green_led_pwm = None
blue_led_pwm = None
initialized = False

logging.info("initializating led!")
if int(ConfigurationReader._led_red_pin) > 0 and int(ConfigurationReader._led_green_pin) > 0 and int(ConfigurationReader._led_blue_pin) > 0 :
	try:
		import RPi.GPIO as GPIO
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(ConfigurationReader._led_red_pin, GPIO.OUT)
		GPIO.setup(ConfigurationReader._led_blue_pin, GPIO.OUT)
		GPIO.setup(ConfigurationReader._led_green_pin, GPIO.OUT)
		        
		#GPIO.output(ConfigurationReader._led_red_pin, red)
		#GPIO.output(ConfigurationReader._led_green_pin, green)
		#GPIO.output(ConfigurationReader._led_blue_pin, blue)
		red_led_pwm = GPIO.PWM(ConfigurationReader._led_red_pin, 100)
		green_led_pwm = GPIO.PWM(ConfigurationReader._led_green_pin, 100)
		blue_led_pwm = GPIO.PWM(ConfigurationReader._led_blue_pin, 100)
		
		red_led_pwm.start(0)
		green_led_pwm.start(0)
		blue_led_pwm.start(0)
		initialized = True
			
	except ImportError:
		logging.error("No GPIO library found! Led  is not enabled!")
else:
	logging.warning("Led not configured!")


# Set a color by giving R, G, and B values of 0-255.
def setLedColor(rgb = []):
	if initialized :
		# Convert 0-255 range to 0-100.
		rgb = [(x / 255.0) * 100 for x in rgb]
		red_led_pwm.ChangeDutyCycle(rgb[0])
		green_led_pwm.ChangeDutyCycle(rgb[1])
		blue_led_pwm.ChangeDutyCycle(rgb[2])


def disabledNode():
	setLedColor([255, 0, 0])


def startingNode():
	setLedColor([225, 0, 0])


def enabledNode():
	setLedColor([0, 255, 0])




