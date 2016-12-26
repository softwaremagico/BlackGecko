import asyncio
import sys
import datetime
import logging

import hangups
import messaging.authentication as authentication
from config import ConfigurationReader
import output.led as led


epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_micros(dt):
	return (dt - epoch).total_seconds() * 1000000.0
	

class Server():
	#Avoid TypeError: can't compare offset-naive and offset-aware datetimes
	_last_text_timestamp = hangups.parsers.from_timestamp(int(unix_time_micros(datetime.datetime.utcnow())))
	_alias = ""
	connected = False
	
	
	def __init__(self):
		self._alias = ConfigurationReader._alias
		self._connect()
		
	
	def _connect(self):
		logging.info("Connecting...")
		# Obtain hangups authentication cookies.
		cookies = authentication.get_auth(ConfigurationReader._refresh_token)

		# Instantiate hangups Client instance.
		self._client = hangups.Client(cookies)
		
		# Add an observer to the on_connect event to run the send_message  when hangups has finished connecting.
		self._client.on_connect.add_observer(lambda: asyncio.async(self._connected()))
		self._client.on_disconnect.add_observer(lambda: asyncio.async(self._disconnected()))
		self._client.on_state_update.add_observer(lambda _: asyncio.async(self._state_updated()))
		
		# Start an asyncio event loop by running Client.connect. This will not return until Client.disconnect is called, or hangups becomes disconnected.
		try:
			loop = asyncio.get_event_loop()
			loop.run_until_complete(self._client.connect())
		except KeyboardInterrupt:
			loop.stop()
			logging.info(ConfigurationReader._alias +" down")
			sys.exit(0)
	
		
	def _disconnect(self):
		asyncio.async(self.send_message("Server '"+ self._alias+"' stopped."))
		yield from self._client.disconnect()


	@asyncio.coroutine	
	def _connected(self):
		logging.info("Server connected!")
		yield from self._get_conversation()		
		asyncio.async(self.send_message("Server '"+ self._alias+"' started."))
		led.startedNode();

	@asyncio.coroutine	
	def _disconnected(self):
		logging.info("Server disconnected!")
	
		
	@asyncio.coroutine	
	def _state_updated(self):
		"""Launched each time the user do anything in the conversation, such us pressing a key, entering into the conversation, etc."""
		yield from self._get_text_message()
		
	def _get_conversation(self):
		logging.debug("Retrieving conversation...")
		#Get users and conversations
		self._user_list, self._conv_list = (
			yield from hangups.build_user_conversation_list(self._client)
		)
		#Get specific conversation defined in configuration
		self._conversation = self._conv_list.get(ConfigurationReader._conversation_id)
		if (self._conversation == None):
			sys.exit("Conversation with id '", ConfigurationReader._conversation_id ,"' not found")
		logging.debug("Conversation found!")
		self.connected = True
		self._conversation.on_event.add_observer(self._conversation_event_launched)
		
		
	def _conversation_event_launched(self, conv_event):
		"""Only launched if the conversation is opened in the other client side when the server is already running"""
		logging.debug("Event on conversation!")
		#yield from self._get_text_message()
		
			
	def _get_text_message(self):
		if (self.connected):
			try:
				conv_events = yield from self._conversation.get_events(None, 1)
			except (IndexError, hangups.NetworkError):
				conv_events = []
			#Search for ChatMessageEvent
			for event in conv_events:
				if isinstance(event, hangups.conversation_event.ChatMessageEvent):
					#Skip own messages
					user = self._conversation.get_user(event.user_id)
					if (event.timestamp > self._last_text_timestamp and not user.is_self):
						self._last_text_timestamp = event.timestamp
						self._text_received(event, user)
						
	def _text_received(self, event, user):
		"""Do nothing"""
		
		
	@asyncio.coroutine
	def send_message(self, message):
		"""Send message using connected hangups. Client instance."""
		# Instantiate a SendChatMessageRequest Protocol Buffer message describing the request.
		request = hangups.hangouts_pb2.SendChatMessageRequest(
			request_header=self._client.get_request_header(),
			event_request_header=hangups.hangouts_pb2.EventRequestHeader(
				conversation_id=hangups.hangouts_pb2.ConversationId(
				id=ConfigurationReader._conversation_id
				),
				client_generated_id=self._client.get_client_generated_id(),
			),
			message_content=hangups.hangouts_pb2.MessageContent(
				segment=[hangups.ChatMessageSegment(message).serialize()],
			),
		)
		# Make the request to the Hangouts API.
		yield from self._client.send_chat_message(request)
		
	
	@asyncio.coroutine
	def send_image(self, text, image_path):
		logging.info("Sending Image...")
		#Upload image and send message with url.
		segments = hangups.ChatMessageSegment.from_str(text)
		try:
			image = open(image_path, 'rb')
			yield from  self._conversation.send_message(segments, image)
			logging.info("Image sended!")
		except FileNotFoundError:
			logging.info("No image to send.")
	

