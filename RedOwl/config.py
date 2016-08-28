import configparser

class ConfigurationReader():
	_configuration_file = 'redowl.conf'
	_conversation_id = ""
	_refresh_token = ""
		
	def __init__(self):
		self.read(ConfigurationReader._configuration_file)
		
	def read(self, file):
		config = configparser.ConfigParser()
		config.read(file)
		
		#Read Server parameters
		server_conf = config['authentication']
		ConfigurationReader._conversation_id = server_conf['conversation_id']
		ConfigurationReader._refresh_token = server_conf['refresh_token']
		
	def write():
		write(ConfigurationReader._configuration_file)
		
	def write(file):
		config = configparser.RawConfigParser()
		config.add_section('authentication')
		config.set('authentication', 'conversation_id', ConfigurationReader._conversation_id)
		config.set('authentication', 'refresh_token', ConfigurationReader. _refresh_token)
		with open(file, 'w') as configfile:
			config.write(configfile)


ConfigurationReader()