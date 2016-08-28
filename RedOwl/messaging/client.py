import asyncio
import hangups
import messaging.authentication as authentication


def connect_to_hangouts(self, refresh_token_path):
	try:
		cookies = hangups.auth.get_auth_stdin(refresh_token_path)
	except hangups.GoogleAuthError as e:
		sys.exit('Login failed ({})'.format(e))

def send_alert(message, auth_token, conversation_id):
	# Obtain hangups authentication cookies.
	# cookies = authentication.get_auth(auth_token)
	cookies = hangups.auth.get_auth_stdin("/home/jorge/workspace/RedOwl/refresh_token.txt")
	print("Cookies: ", cookies)

	# Instantiate hangups Client instance.
	client = hangups.Client(cookies)

	# Add an observer to the on_connect event to run the send_message coroutine
	# when hangups has finished connecting.
	client.on_connect.add_observer(lambda: asyncio.async(send_message(client, message, conversation_id)))

	# Start an asyncio event loop by running Client.connect. This will not
	# return until Client.disconnect is called, or hangups becomes
	# disconnected.
	loop = asyncio.get_event_loop()
	loop.run_until_complete(client.connect())

@asyncio.coroutine
def send_message(client, message, conversation_id):
	"""Send message using connected hangups.Client instance."""

	# Instantiate a SendChatMessageRequest Protocol Buffer message describing
	# the request.
	request = hangups.hangouts_pb2.SendChatMessageRequest(
		request_header=client.get_request_header(),
		event_request_header=hangups.hangouts_pb2.EventRequestHeader(
			conversation_id=hangups.hangouts_pb2.ConversationId(
			id=conversation_id
			),
			client_generated_id=client.get_client_generated_id(),
		),
		message_content=hangups.hangouts_pb2.MessageContent(
			segment=[hangups.ChatMessageSegment(message).serialize()],
		),
	)
	
	try:
		# Make the request to the Hangouts API.
		yield from client.send_chat_message(request)
	finally:
		# Disconnect the hangups Client to make client.connect return.
		yield from client.disconnect()
