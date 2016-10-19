<img src="./images/redowl.png" width="128" alt="RedOwl" align="middle">

# Redowl
Basic home intrussion detection system based in Hangouts and a Raspberry Pi. When an intrussion has been detected, it sends a hangouts message as an alarm. 

This project is based on the [hangups] (https://github.com/tdryer/hangups) API for Google Hangouts. It has been developed as a continuation of the [Beholder](https://github.com/jorgehortelano/beholder) project, that uses Whatsapp instead of Google Hangouts.

This software has been developed using a Raspberry Pi 2 Model B with a LM393 Sound Detection Sensor Module and a Pyroelectric Infrared PIR Motion Sensor Detector Module HC-SR501. The operating system is an Ubuntu Mate 16.04.

## Dependencies
  1. Python 3.3+
  2. GPIO library for sensors
  3. Hangups api for python
  4. cv2

## Installation

Install [hangups](https://github.com/tdryer/hangups) simply typing:
```
pip3 install hangups.
```
But I would recommend to install last version of hangups. Then:
```
git clone https://github.com/tdryer/hangups.git
cd hangups
python3 setup.py
```

After installing hangups API. Install this application running inside the application folder the next command:
```
python setup.py install
```
### Installing using a debian package
The application has a script for generating a debian package. If you prefer to install on this way, please, install first `debuild`, `devscripts` and `debhelper`. This package can be installed using `apt-get install <package>`.

After this, you can execute the package generator script as follows:
```
sudo ./package.sh
```

## Configuration
The basic configuration file is in `/etc/redowl.conf`. This configuration file will be copied to the user local configuration the first time the application is launched. If you want to have different users with different configuration, then edit `/home/<user>/.config/RedOWl/redowl.conf`.

In both cases, the configuration file will have this fields:

	[authentication]
	conversation_id = XXXXXXXXXXXXXXXXXXXXXXXXX
	refresh_token = /home/<user>/.cache/hangups/refresh_token.txt

	[node]
	alias = RaspCam
	log_path = /tmp/RedOwl.log

	[sensors]
	infrared_pin = 0
	sound_pin = 0

The most important fields are the one in `[authenticaion]`: `refresh_token` and `conversation_id`.

### Obtaining the refresh_token

The refresh token is needed to use the API with Google. To obtain it, execute hangups one time:
```
hangups
```

It will show a link to ask for this refresh token. Perform all required tasks showed in the console. Execute it again to check that now hangups runs correctly and you can see the command-line client for hangouts. If it is not working, see the hangups [documentation](https://github.com/tdryer/hangups).

It it is working, you can see a file called `refresh_token.txt` created by hangups at `/home/<user>/.cache/hangups/`. Set the path to this file into the `redowl.conf` configuration file. 

### ___Note___

___In some cases, google launches a 400 error (OAuth2 error). In this case, follow this instructions:___

1. ___Go to this url___ [url](https://accounts.google.com/o/oauth2/programmatic_auth?hl=en&scope=https%3A%2F%2Fwww.google.com%2Faccounts%2FOAuthLogin+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email&client_id=936475272427.apps.googleusercontent.com&access_type=offline&delegated_client_id=183697946088-m3jnlsqshjhh5lbvg05k46q1k4qqtrgn.apps.googleusercontent.com&top_level_cookie=1)
2. ___Enter your username, click next.___
3. ___Right click page background, inspect___
4. ___Go to the network tab.___
5. ___Enter your password, click sign in___
6. ___Click the first row, the one that says "programmatic_auth"___
7. ___Scroll down in the right-side panel, find "set-cookie"___
8. ___Your code should be there, after "oauth_code=", up to but not including the semicolon.___
9. ___Copy it and use it.___

### Selecting the conversation

After obtaining the refresh token, the conversation id can be obtained if you run the application with:
```
redowl --conversations-info
```

This will show a list with all conversations id available. Try one by one until you are connected to the correct conversation. 

### Testing the configuration

For testing it, you can use:
```
redowl --test-alert
```
This command will send a 'Test message' text to the selected conversation. 

## Execution

To launch the application as a server execute:

	redowl -c
	

If everything is running correctly, now you can use a standard hangouts client (i.e. in your mobile phone) to communicate with the application. You can use the next messages as commands:

	hello			will show the name (alias) of the device.
	select <alias>	select the device to accept other commands.
	enable			start the sensor detection for the selected device.
	disable			stops sending alerts from sensors.
	help            shows these options.

For using this application at least you need to select the node first, and then start the detection. 

## Multiuser

Each time a user want to access to the alerts system, must "subscribe" to the node with the `enable` command. He will automatically receive any alerts that will be launched from the system. Also, if later the user executes the `disable` command, he will stop receiving any alert. But this command does not affect any other subscribed user that still will be suscribed to the alert system. 
