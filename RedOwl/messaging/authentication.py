import hangups.auth as auth

def get_auth(refresh_token_path):
	return auth.get_auth_stdin(refresh_token_path)
