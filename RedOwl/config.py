import configparser
import appdirs
import os

class ConfigurationReader():
	_config_file = 'redowl.conf'
	_app_dirs = appdirs.AppDirs('RedOWl', 'softwaremagico')
	_conversation_id = ""
	_refresh_token = ""
	_alias = ""
	_infrared_sensor_pin = 0
	_sound_sensor_pin = 0
	_log_file = ""
	_cascade_file = ""


	def __init__(self):
		config_file = ConfigurationReader.get_config_file_path()
		if (os.path.isfile(config_file)):
			#User folder configuration file.
			self.read(config_file)
		elif(os.path.isfile("/etc/redowl/"+ConfigurationReader._config_file)):
			#System configuration file.
			self.read("/etc/redowl/"+ConfigurationReader._config_file)
		else:
			#Application configuration file.
			self.read(ConfigurationReader._config_file)		


	def read(self, file):
		config = configparser.ConfigParser()
		config.read(file)
		
		#Read Server parameters
		server_conf = config['authentication']
		ConfigurationReader._conversation_id = server_conf['conversation_id']
		ConfigurationReader._refresh_token = server_conf['refresh_token']
		
		server_conf = config['node']
		ConfigurationReader._alias = server_conf['alias']
		ConfigurationReader._log_file = server_conf['log_path']
		
		server_conf = config['sensors']
		ConfigurationReader._infrared_sensor_pin = int(server_conf['infrared_pin'])
		ConfigurationReader._sound_sensor_pin = int(server_conf['sound_pin'])
		
		server_conf = config['face_detection']
		ConfigurationReader._frame_width = int(server_conf['frame_width'])
		ConfigurationReader._frame_heigh = int(server_conf['frame_heigh'])
		ConfigurationReader._cascade_file = server_conf['haarcascade_file']


	def write_user_folder():
		#Create user config folder if not exists
		if not os.path.exists(ConfigurationReader._app_dirs.user_config_dir):
			os.makedirs(ConfigurationReader._app_dirs.user_config_dir)
		open(ConfigurationReader.get_config_file_path(), 'a').close()
		#Store always in user config folder
		ConfigurationReader.write(ConfigurationReader.get_config_file_path())


	def get_config_file_path():
		# Build default paths for files.
		return os.path.join(ConfigurationReader._app_dirs.user_config_dir, ConfigurationReader._config_file)


	def write(file):
		config = configparser.RawConfigParser()
		config.add_section('authentication')
		config.set('authentication', 'conversation_id', ConfigurationReader._conversation_id)
		config.set('authentication', 'refresh_token', ConfigurationReader. _refresh_token)
		with open(file, 'w') as configfile:
			config.write(configfile)


ConfigurationReader()