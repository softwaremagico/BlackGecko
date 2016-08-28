import hangups.auth as auth


def get_auth(access_token):
	return auth._get_session_cookies(access_token)