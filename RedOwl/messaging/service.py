import hangups

def connect_to_hangouts(self, refresh_token_path):
	try:
		cookies = hangups.auth.get_auth_stdin(refresh_token_path)
	except hangups.GoogleAuthError as e:
		sys.exit('Login failed ({})'.format(e))