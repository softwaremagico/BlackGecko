import os
import argparse
import logging
import sys

import messaging.alert_client
from extras.echo_server import EchoServer
from extras.conversations_info import ConversationsInfo
from messaging.command_server import CommandServer
from config import ConfigurationReader

_echo_server = False
_test_alert = False
_command_server = False
_conversations_info = False

logging.basicConfig(filename=ConfigurationReader._log_file, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def main():
	"""Main entry point."""
	handle_arguments()
	
	
	logging.info("RedOwl starting....")
	
	if (_echo_server):
		EchoServer()
	elif (_test_alert):
		messaging.alert_client.send_alert('Test message')
	elif(_command_server):
		CommandServer()
	elif(_conversations_info):
		ConversationsInfo()
	
	#message_service.connect_to_hangouts()
	logging.info("RedOwl closing....")
	
def handle_arguments():
	parser = argparse.ArgumentParser(description='An alarm system based on Hangouts.', epilog="Copyright© 2016 Jorge Hortelano")
	
	parser.add_argument('-f', '--configuration-file', help='Selects a specific configuration file.')
	
	#Exclusive options (different executions available)
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-e', '--echo-server', action='store_true', help='Enables echo server for testing communications.')
	group.add_argument('-t', '--test-alert', action='store_true', help='Sends a simple predefined text message to the hangouts conversation.')
	group.add_argument('-c', '--command-server', action='store_true', help='Starts a server that can execute commands for the OS.')
	group.add_argument('-i', '--conversations-info', action='store_true', help='Shows all available conversations ids.')

	args = parser.parse_args()
	
	if(args.configuration_file):
		ConfigurationReader().read(args.configuration_file)
	
	if (args.echo_server):
		global _echo_server
		_echo_server = True
		
	if (args.test_alert):
		global _test_alert
		_test_alert = True
		
	if(args.command_server):
		global _command_server
		_command_server = True
		
	if(args.conversations_info):	
		global _conversations_info
		_conversations_info = True

#Execute as standard main like C++
if __name__ == '__main__':
	main()
