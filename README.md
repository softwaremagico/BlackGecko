<img src="./images/blackgecko.png" width="128" alt="BlackGecko" align="middle">

# BlackGecko

Basic home intrusion detection system using a Raspberry Pi. Combines OpenCV and sensors input for detecting intrusions,
and it uses hangouts (hangups API) to send a message as an alarm.

### Why use BlackGecko?

Different projects exists for converting your Raspberry Pi in a security Camera. One of them is motion (and motionEye).
The big advantage from this project compared to them, is that we have communication integrated on a Push service. That
means that you can connect and communicate without the need of a __public IP__. This is the case if your ISP is using a
CG-NAT. With BlackGecko, you will be able to send commands to your Raspberry Pi, launch alarms and integrate others
Raspberry Pi modules if required.

### History

This project is based on the [hangups] (https://github.com/tdryer/hangups) API for Google Hangouts. It has been
developed as a continuation of the [Beholder](https://github.com/jorgehortelano/beholder) project, that uses Whatsapp
instead of Google Hangouts. As Whatsapp security has been increased, 3rd party applications are not allowed to connect.

This software has been developed using a Raspberry Pi 2 Model B with a LM393 Sound Detection Sensor Module, and a
Pyroelectric Infrared PIR Motion Sensor Detector Module HC-SR501. The operating system is an Ubuntu Mate 16.04.

## Dependencies

1. Python 3.3+
2. GPIO library for sensors
3. Hangups api for python
4. cv2
5. picamera

## Installation

Install first [hangups](https://github.com/tdryer/hangups) simply typing:

```
pip3 install hangups
```

But I would recommend to install last version of hangups. Then download the code and install it:

```
git clone https://github.com/tdryer/hangups.git
cd hangups
python3 setup.py install
```
If it fails, maybe you need to install some python dependencies:

```
pip3 install multidict typing_extensions attr yarl
```

And run the `install` command again. 

After installing hangups API. Install also the picamera module:

```
pip3 install "picamera[array]"
```

Install also cv2. For this,

```
pip3 install opencv-python
pip3 install numpy -I
```

Next, install `apt install libatlas-base-dev`. You can check if the installation is correct, just
typing `python3 -c "import cv2"`. If no error is shown, then everything is installed correctly. 

Now install BlackGecko application typing inside the application folder using the next command:

```
python3 setup.py install
```

### Creating a debian package

The application has a script for generating a debian package. If you prefer to install on this way, please, install
first `debuild`, `devscripts` and `debhelper`. This package can be installed using `apt-get install <package>`.

After this, you can execute the package generator script as follows:

```
sudo ./package.sh
```

### Executing from command line

If you do not want -or you cannot- use the provided package, still you can run the application manually. On the root
folder of the project, execute:

```
python BlackGecko
``` 

Now, generate the configuration file as described on the next section.

# Configuration

The basic configuration file is in `/etc/blackgecko.conf` or `/etc/blackgecko/blackgecko.conf`. This configuration file
will be copied to the user local configuration the first time the application is launched. If you want to have different
users with different configuration, then edit `/home/<user>/.config/RedOWl/blackgecko.conf`.

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

It will show a link to ask for this refresh token. Perform all required tasks showed in the console. Execute it again to
check that now hangups runs correctly and you can see the command-line client for hangouts. If it is not working, see
the hangups [documentation](https://github.com/tdryer/hangups).

If it is working, you can see a file called `refresh_token.txt` created by hangups at `/home/<user>/.cache/hangups/`.
Set the path to this file into the `blackgecko.conf` configuration file.

### Solving issues with hangups

If you cannot log in, you can try to do a manual login. For this purpose, execute the script
on `hangups/hangups_manual_login.py`:

```
python hangups_manual_login.py
```

Now open the link on the provided URL. This will give permission to the application to access to you google account with
an oath2 token.

If you get a infinite "One moment please...":

1. Click again on the URL provided by the script
2. Enter your username, click next.
3. Right click page background, inspect
4. Go to the network tab.
5. Enter your password, click sign in
6. Click the first row, the one that says "programmatic_auth"
7. Scroll down in the right-side panel, find "set-cookie"
8. Your code should be there, after "oauth_code=", up to but not including the semicolon.
9. Copy it and use it on the input of the script.

After this, you can run again `hangups`.

### Selecting the conversation

After obtaining the refresh token, the conversation id can be obtained if you run the application with:

```
blackgecko --conversations-info
```

This will show a list with all conversations' id available. Try one by one until you are connected to the correct
conversation.

### Testing the configuration

For testing it, you can use:

```
blackgecko --test-alert
```

or inside the project folder run:

```
python3 BlackGecko --test-alert
```

This command will send a 'Test message' text to the selected conversation.

## Execution

To launch the application as a server execute:

```
blackgecko -c
```

or inside the project folder run:

```
python3 BlackGecko -c
```

If everything is running correctly, now you can use a standard Hangouts client (i.e. in your mobile phone) to
communicate with the application. You can use the next messages as commands:

	hello			will show the name (alias) of any connected device.
	select <alias>	select one device to accept other commands. 'Select all' will select all avaialble devices.
	enable			start the sensor detection for the selected device.
	disable			stops sending alerts from sensors.
	help            shows these options.

For using this application at least you need to select the node first, and then start the detection.

### Example of execution

For example, to run the first time, you will have some chats like this in your Google chat:

    <user> hello
    <blackgecko> Hello from 'blackgecko'!
    <user> select all
    <blackgecko> Selecting node 'blackgecko'
    <user> enable
    <blackgecko> Sensors in 'blackgecko' enabled  🏁
    ...

## Multiuser

Each time a user want to access to the alerts' system, must "subscribe" to the node with the `enable` command. He will
automatically receive any alerts that will be launched from the system. Also, if later the user executes the `disable`
command, he will stop receiving any alert, but this command does not affect any other subscribed user that still will be
subscribed to the alert system.

# Creating a service

If you are not using the default deb package, you need to create the service yourself. For creating a system daemon, in
the `service` folder you have a template `blackgecko.servuce`. Update the `ExecStart` and `User` lines with the correct
path to the downloaded sourcecode of BlackGecko, and the user that will run it.

Copy it to `/etc/systemd/system/blackgecko.service` and enable it by typing:

```
systemctl enable blackgecko
systemctl daemon-reload
systemctl start blackgecko
```
