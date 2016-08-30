import configparser
import appdirs
import os

class ConfigurationReader():
	_config_file = 'redowl.conf'
	_app_dirs = appdirs.AppDirs('RedOWl', 'softwaremagico')
	_conversation_id = ""
	_refresh_token = ""
	_alias = ""


	def __init__(self):
		config_file = ConfigurationReader.get_config_file_path()
		if (os.path.isfile(config_file)):
			self.read(config_file)
		else:
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