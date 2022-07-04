import asyncio
import logging


from config import ConfigurationReader
from .server import Server


class EchoServer(Server):
	
	
	def _text_received(self, event, user):
		logging.info("Text received '" + event.text + "'.")		
		asyncio.ensure_future(self.send_message(event.text))
		
