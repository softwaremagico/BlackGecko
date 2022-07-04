<img src="./images/blackgecko.png" width="128" alt="BlackGecko" align="middle">

# BlackGecko
Basic home intrussion detection system using a Raspberry Pi. Combines OpenCV and sensors input for detecting intrussions, and it uses hangouts (hangups API) to send a message as an alarm. 

This project is based on the [hangups] (https://github.com/tdryer/hangups) API for Google Hangouts. It has been developed as a continuation of the [Beholder](https://github.com/jorgehortelano/beholder) project, that uses Whatsapp instead of Google Hangouts.

This software has been developed using a Raspberry Pi 2 Model B with a LM393 Sound Detection Sensor Module and a Pyroelectric Infrared PIR Motion Sensor Detector Module HC-SR501. The operating system is an Ubuntu Mate 16.04.

## Dependencies
  1. Python 3.3+
  2. GPIO library for sensors
  3. Hangups api for python
  4. cv2
  5. picamera

## Installation

Install first [hangups](https://github.com/tdryer/hangups) simply typing:
```
pip3 install hangups.
```
But I would recommend to install last version of hangups. Then download the code and install it:
```
git clone https://github.com/tdryer/hangups.git
cd hangups
python3 setup.py install
```

After installing hangups API. Install also the picamera module:
```
pip3 install "picamera[array]"
```

Now install BlackGecko application typing inside the application folder the next command:
```
python setup.py install
```
### Installing using a debian package
The application has a script for generating a debian package. If you prefer to install on this way, please, install first `debuild`, `devscripts` and `debhelper`. This package can be installed using `apt-get install <package>`.

After this, you can execute the package generator script as follows:
```
sudo ./package.sh
```

### Executing from command line
If you do not want -or you cannot- use the provided package, still you can run the application manually. On the root folder of the project, execute:

```
python BlackGecko
``` 

And generate the configuration file as described on the next section. 

# Configuration
The basic configuration file is in `/etc/blackgecko.conf` or `/etc/blackgecko/blackgecko.conf`. This configuration file will be copied to the user local configuration the first time the application is launched. If you want to have different users with different configuration, then edit `/home/<user>/.config/RedOWl/blackgecko.conf`.

In both cases, the configuration file will have this fields:

	[authentication]
	conversation_id = XXXXXXXXXXXXXXXXXXXXXXXXX
	refresh_token = /home/<user>/.cache/hangups/refresh_token.txt

	[node]
	alias = RaspCam
	log_path = /tmp/BlackGecko.log

	[sensors]
	infrared_pin = 0
	sound_pin = 0
	
	[output]
	buzzer_pin = 0
	led_red_pin = 0
	led_blue_pin = 0
	led_green_pin = 0
	
	[face_detection]
	frame_width = 0
	frame_heigh = 0
	haarcascade_file = ''
	rotate_image = ''

The most important fields are the one in `[authenticaion]`: `refresh_token` and `conversation_id`.

### Obtaining the refresh_token

The refresh token is needed to use the API with Google. To obtain it, execute hangups one time:
```
hangups
```

It will show a link to ask for this refresh token. Perform all required tasks showed in the console. Execute it again to check that now hangups runs correctly and you can see the command-line client for hangouts. If it is not working, see the hangups [documentation](https://github.com/tdryer/hangups).

It it is working, you can see a file called `refresh_token.txt` created by hangups at `/home/<user>/.cache/hangups/`. Set the path to this file into the `blackgecko.conf` configuration file. 

### Solving issues with hangups
If you cannot login, you can try to do a manual login. For this purpose, execute the script on `hangups/hangups_manual_login.py`:

```
python hangups_manual_login.py
```

And open the link on the provided URL. This will give permission to the application to access to you google account with an oath2 token. 

If you get a infinite "One moment please...":
1. ___Click again on the URL provided by the script__
2. ___Enter your username, click next.___
3. ___Right click page background, inspect___
4. ___Go to the network tab.___
5. ___Enter your password, click sign in___
6. ___Click the first row, the one that says "programmatic_auth"___
7. ___Scroll down in the right-side panel, find "set-cookie"___
8. ___Your code should be there, after "oauth_code=", up to but not including the semicolon.___
9. ___Copy it and use it on the input of the script.___

And after this, you can run again `hangups`.

### Selecting the conversation

After obtaining the refresh token, the conversation id can be obtained if you run the application with:
```
blackgecko --conversations-info
```
This will show a list with all conversations id available. Try one by one until you are connected to the correct conversation. 

### Testing the configuration

For testing it, you can use:
```
blackgecko --test-alert
```
This command will send a 'Test message' text to the selected conversation. 

## Execution

To launch the application as a server execute:
```
blackgecko -c
```
If everything is running correctly, now you can use a standard hangouts client (i.e. in your mobile phone) to communicate with the application. You can use the next messages as commands:

	hello			will show the name (alias) of any connected device.
	select <alias>	select one device to accept other commands. 'Select all' will select all avaialble devices.
	enable			start the sensor detection for the selected device.
	disable			stops sending alerts from sensors.
	help            shows these options.

For using this application at least you need to select the node first, and then start the detection. 

## Multiuser

Each time a user want to access to the alerts system, must "subscribe" to the node with the `enable` command. He will automatically receive any alerts that will be launched from the system. Also, if later the user executes the `disable` command, he will stop receiving any alert. But this command does not affect any other subscribed user that still will be suscribed to the alert system. 
