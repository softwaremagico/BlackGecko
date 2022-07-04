#This is obtained from the examples of the hangups application.

import asyncio
import hangups
import messaging.authentication as authentication
from config import ConfigurationReader


def connect_to_hangouts(self):
	try:
		cookies = hangups.auth.get_auth_stdin(ConfigurationReader._refresh_token)
	except hangups.GoogleAuthError as e:
		sys.exit('Login failed ({})'.format(e))

def send_alert(message):
	# Obtain hangups authentication cookies.
	cookies = authentication.get_auth(ConfigurationReader._refresh_token)

	# Instantiate hangups Client instance.
	client = hangups.Client(cookies)

	# Add an observer to the on_connect event to run the send_message  when hangups has finished connecting.
	client.on_connect.add_observer(lambda: asyncio.ensure_future(send_message(client, message)))

	# Start an asyncio event loop by running Client.connect. This will not
	# return until Client.disconnect is called, or hangups becomes
	# disconnected.
	loop = asyncio.get_event_loop()
	loop.run_until_complete(client.connect())

@asyncio.coroutine
def send_message(client, message):
	"""Send message using connected hangups. Client instance."""

	# Instantiate a SendChatMessageRequest Protocol Buffer message describing the request.
	request = hangups.hangouts_pb2.SendChatMessageRequest(
		request_header=client.get_request_header(),
		event_request_header=hangups.hangouts_pb2.EventRequestHeader(
			conversation_id=hangups.hangouts_pb2.ConversationId(
			id=ConfigurationReader._conversation_id
			),
			client_generated_id=client.get_client_generated_id(),
		),
		message_content=hangups.hangouts_pb2.MessageContent(
			segment=[hangups.ChatMessageSegment(message).serialize()],
		),
	)
	
	try:
		# Make the request to the Hangouts API.
		print("Sending message '", message, "'.")
		yield from client.send_chat_message(request)
	finally:
		# Disconnect the hangups Client to make client.connect return.
		yield from client.disconnect()
