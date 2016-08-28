import os
import appdirs
import configargparse
import messaging.service as message_service
from config import ConfigurationReader

def main():
	"""Main entry point."""
	print("RedOwl starting....")
	# Build default paths for files.
	dirs = appdirs.AppDirs('RedOWl', 'softwaremagico')
	default_config_path = 'redowl.conf'
	user_config_path = os.path.join(dirs.user_config_dir, default_config_path)

	#Define commands
	parser = configargparse.ArgumentParser(
	prog='hangups', default_config_files=[default_config_path, user_config_path],
	formatter_class=configargparse.ArgumentDefaultsHelpFormatter,
	add_help=False,  # Disable help so we can add it to the correct group.
	)
	general_group = parser.add_argument_group('General')
	general_group.add('-h', '--help', action='help',
		help='show this help message and exit')

	#Read config file
	configurationReader = ConfigurationReader('redowl.conf')
	
	
	#message_service.connect_to_hangouts()
	print("RedOwl closing....")

#Execute as standard main like C++
if __name__ == '__main__':
	main()
