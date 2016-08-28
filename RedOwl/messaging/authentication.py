import hangups
from config import ConfigurationReader

def get_auth(refresh_token):
	return hangups.auth.get_auth_stdin(refresh_token)

def store_refresh_token(refresh_token_filename, refresh_token):
	ConfigurationReader._refresh_token = refresh_token
	ConfigurationReader.write('redowl.conf')
	
def load_refresh_token(refresh_token_filename):
	return ConfigurationReader._refresh_token

#Some Monkey Patch
#Override the method to read refresh_token from config file
#Override the method to store refresh_token in config file
hangups.auth._load_oauth2_refresh_token = load_refresh_token
hangups.auth._save_oauth2_refresh_token = store_refresh_token
