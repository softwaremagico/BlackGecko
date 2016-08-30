import os
import argparse
import logging

import messaging.alert_client
from extras.echo_server import EchoServer
from messaging.command_server import CommandServer
from config import ConfigurationReader

_echo_server = False
_test_alert = False
_command_server = False

logging.basicConfig(filename=ConfigurationReader._log_file, level=logging.INFO)

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
	
	#message_service.connect_to_hangouts()
	logging.info("RedOwl closing....")
	
def handle_arguments():
	parser = argparse.ArgumentParser(description='An alarm system based on Hangouts.', epilog="Copyright© 2016 Jorge Hortelano")
	
	#Exclusive options (different executions available)
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--echo-server', '-e', action='store_true', help='Enables echo server for testing communications.')
	group.add_argument('--test-alert', '-t', action='store_true', help='Sends a simple predefined text message to the hangouts conversation.')
	group.add_argument('--command-server', '-c', action='store_true', help='Starts a server that can execute commands for the OS.')

	args = parser.parse_args()
	
	if (args.echo_server):
		global _echo_server
		_echo_server = True
		
	if (args.test_alert):
		global _test_alert
		_test_alert = True
		
	if(args.command_server):
		global _command_server
		_command_server = True
		

#Execute as standard main like C++
if __name__ == '__main__':
	main()
