import asyncio
import sys
import datetime

import hangups
import messaging.authentication as authentication
from config import ConfigurationReader



class ConversationsInfo():
	
	def __init__(self):
		self._connect()
	
	
	def _connect(self):
		print("Connecting...")
		# Obtain hangups authentication cookies.
		cookies = authentication.get_auth(ConfigurationReader._refresh_token)

		# Instantiate hangups Client instance.
		self._client = hangups.Client(cookies)
		
		# Add an observer to the on_connect event to run the send_message  when hangups has finished connecting.
		self._client.on_connect.add_observer(lambda: asyncio.ensure_future(self._connected()))
		self._client.on_disconnect.add_observer(lambda: asyncio.ensure_future(self._disconnected()))
		
		# Start an asyncio event loop by running Client.connect. This will not return until Client.disconnect is called, or hangups becomes disconnected.
		loop = asyncio.get_event_loop()
		loop.run_until_complete(self._client.connect())
	
	
	@asyncio.coroutine	
	def _disconnect(self):
		yield from self._client.disconnect()


	@asyncio.coroutine	
	def _connected(self):
		yield from self._get_conversations()		
		

	@asyncio.coroutine	
	def _disconnected(self):
		print("Disconnected!")
	
		
	def _get_conversations(self):
		print("Retrieving conversations:")
		#Get users and conversations
		self._user_list, self._conv_list = (
			yield from hangups.build_user_conversation_list(self._client)
		)

		#Show conversations id.
		for conversation in self._conv_list.get_all():
			print("\tConversation found:", conversation.id_)
		
		#Disconnect
		asyncio.ensure_future(self._disconnect())