# Redowl
Basic alarm system based in Python and a Raspberry Pi. It has been developed as a continuation of the [Beholder](https://github.com/jorgehortelano/beholder) project, that uses Whatsapp instead of Google Hangouts.

This project is based on the [hangups] (https://github.com/tdryer/hangups) API for Google Hangouts.

This software has been developed using a Raspberry Pi 2 Model B with a LM393 Sound Detection Sensor Module and a Pyroelectric Infrared PIR Motion Sensor Detector Module HC-SR501. The operating system is an Ubuntu Mate 16.04.

## Dependencies
  1. Python 3.3+
  2. Hangups api for python

## Installation

Install [hangups](https://github.com/tdryer/hangups) simply typing:
```
pip3 install hangups.
```

After installing hangups API. Install this application running inside the application folder the next command:
```
python setup.py install
```

## Config


## Execution

To launch the application execute:

	redowl -c
	

If everything is running, from your hangouts application, you can use the next messages as commands:

	hello			will show the name (alias) of the device.
	select <alias>	select the device to accept other commands.
	enable			start the sensor detection for the selected device.
	disable			stops sending alerts from sensors.
	help            shows these options.

For using this application at least you need to select the node first, and then start the detection. 

## Multiuser

Different users that are in `allowed_users` list can receive the alert messages. 

Each time a user want to access to the alerts system, must "subscribe" to the node with the `enable` command. He will automatically receive any alerts that will be launched from the system. Also, if later the user executes the `disable` command, he will stop receiving any alert. But this command does not affect any other subscribed user that still will be suscribed to the alert system. 
