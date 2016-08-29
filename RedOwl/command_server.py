import asyncio
import sys
import datetime
import hangups
import messaging.authentication as authentication
from config import ConfigurationReader

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_micros(dt):
	return (dt - epoch).total_seconds() * 1000000.0



class CommandServer():
	#Avoid TypeError: can't compare offset-naive and offset-aware datetimes
	_last_text_timestamp = hangups.parsers.from_timestamp(int(unix_time_micros(datetime.datetime.utcnow())))
	connected = False
	
	
	def __init__(self):
		self._connect()
	
	
	def _connect(self):
		print("Connecting...")
		# Obtain hangups authentication cookies.
		cookies = authentication.get_auth(ConfigurationReader._refresh_token)

		# Instantiate hangups Client instance.
		self._client = hangups.Client(cookies)
		
		# Add an observer to the on_connect event to run the send_message  when hangups has finished connecting.
		self._client.on_connect.add_observer(lambda: asyncio.async(self._connected()))
		self._client.on_disconnect.add_observer(lambda: asyncio.async(self._disconnected()))
		self._client.on_state_update.add_observer(lambda _: asyncio.async(self._state_updated()))
		
		# Start an asyncio event loop by running Client.connect. This will not
		# return until Client.disconnect is called, or hangups becomes
		# disconnected.
		loop = asyncio.get_event_loop()
		loop.run_until_complete(self._client.connect())
	
		
	def _disconnect(self):
		self._client.disconnect()


	@asyncio.coroutine	
	def _connected(self):
		print("Server connected:")
		self.connected = True
		yield from self._get_conversation()		
		

	@asyncio.coroutine	
	def _disconnected(self):
		print("Server disconnected!")
	
	
	@asyncio.coroutine	
	def _state_updated(self):
		"""Launched each time the user do anything in the conversation, such us pressing a key, entering into the conversation, etc."""
		#print("--> State updated!")
		yield from self._get_text_message()
	
		
	def _get_conversation(self):
		print("\t- Retrieving conversation")
		#Get users and conversations
		self._user_list, self._conv_list = (
			yield from hangups.build_user_conversation_list(self._client)
		)
		#Get specific conversation defined in configuration
		self._conversation = self._conv_list.get(ConfigurationReader._conversation_id)
		if (self._conversation == None):
			sys.exit("Conversation with id '", ConfigurationReader._conversation_id ,"' not found")
		print("\t- Conversation found!")
		self._conversation.on_event.add_observer(self._conversation_event_launched)
		
		
	def _conversation_event_launched(self, conv_event):
		"""Only launched if the conversation is opened in the other client side when the server is already running"""
		#print("--> Event on conversation!")
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
					if (event.timestamp > self._last_text_timestamp):
						self._last_text_timestamp = event.timestamp
						self._text_received(event.text)
						
	
	def _text_received(self, text):
		print("Text received: ", text)
	
CommandServer()