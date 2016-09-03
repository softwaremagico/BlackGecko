import asyncio
import subprocess
import logging

from sensors.sensors import SensorsController
from config import ConfigurationReader
from .server import Server


class CommandServer(Server):
	_node_enabled = []
	_user_selection = []
	_events_initialized = False
	
	
	def __init__(self):
		self._alias = ConfigurationReader._alias
		self._connect()
						
	
	def _text_received(self, event, user):
		logging.info("Text received '" + event.text + "' from user '" + str(user.emails) + "'.")		
		if "help" ==  event.text.lower():
			self.show_help()
		#Node list
		elif "hello" ==  event.text.lower(): 
			asyncio.async(self.send_message("Hello from '" + self._alias+"'!"))
		#get status
		elif "status" in event.text.lower():
			self.send_status(user)
		#Enable/Disable node if needed.
		elif "unselect" in event.text.lower():
			if (self._alias.lower() in event.text.lower() or 'all' in event.text.lower()):
				self._unselect_node(user)
		elif "select" in event.text.lower():
			if (self._alias.lower() in event.text.lower() or 'all' in event.text.lower()):
				self._select_node(user)
		elif "disable" ==  event.text.lower():
			if (self.is_node_selected(user)) :
				self._disable_node(user)
		elif "enable" ==  event.text.lower():
			if (self.is_node_selected(user)) :
				self._enable_node(user)
		# Execute command if possible.
		elif event.text.lower() == "reboot":
			if (self.is_node_selected(user)) :
				command = ['sudo', 'reboot']
				self.execute_command(command)
		else:
		# just print info
			if (self.is_node_selected(user)) :
				logging.warning("Invalid command '" + event.text +"' from '" + str(user.id_) +"'.")
				asyncio.async(self.send_message("Invalid command '" + event.text + "'."))

	
	def _select_node(self, user):
		logging.info("Selecting node '" + self._alias + "' for user '" + str(user.emails) + "'")
		self._user_selection.append(user.id_)
		asyncio.async(self.send_message("Selecting node '" + self._alias +"'"))


	def _unselect_node(self, user):
		if (user.id_ in self._user_selection):
			logging.info("Unselecting node '" + self._alias + "' for user '" + str(user.emails) + "'")
			self._user_selection.remove(user.id_)
			asyncio.async(self.send_message("Unselecting node '" + self._alias +"'"))
	
	
	def is_node_selected(self, user):
		return user.id_ in self._user_selection
		
		
	def is_node_enabled(self, user):
		return user.id_ in self._node_enabled
	
	def _disable_node(self, user):
		if user.id_ in self._node_enabled: 
			self._node_enabled.remove(user.id_)
			logging.info("Disabling node '" + self._alias +  "'")
			asyncio.async(self.send_message("Disabling node '" + self._alias + "'"))
	
			
	def _enable_node(self, user):
		if user.id_ not in self._node_enabled:
			self._node_enabled.append(user.id_)
			logging.info("Enabling node '" + self._alias + "'.")
			SensorsController(self.send_message)

		
	def show_help(self):
		asyncio.async(self.send_message("Available commands:\n\thello\n\tstatus\n\tselect <alias | all>\n\tenable\n\tdisable"))
	
		
	def send_status(self, user):
		if self.is_node_selected(user):
			selected = " [Selected]"
		else:
			selected = ""
		if self.is_node_enabled(user):
			enabled = "enabled"
		else:
			enabled = "disabled"
		asyncio.async(self.send_message("Node '" + self._alias + "'"+selected+": " + enabled))
		
	
	#Executes a command if the user is in the allowed_user list. 
	def execute_command(self, command):	
		status = subprocess.check_output(command)
		self.send_message("Executing '" + str(command)+"'.")
		logging.debug("Status: " + status)
		asyncio.async(self.send_message(status))
		
