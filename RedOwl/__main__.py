import os
import argparse
import messaging.alert_client
from extras.echo_server import EchoServer

_echo_server = False
_test_alert = False

def main():
	"""Main entry point."""
	handle_arguments()
	
	
	print("RedOwl starting....")
	
	if (_echo_server):
		EchoServer()
	elif (_test_alert):
		messaging.alert_client.send_alert('Test message')
	
	#message_service.connect_to_hangouts()
	print("RedOwl closing....")
	
def handle_arguments():
	parser = argparse.ArgumentParser(description='An alarm system based on Hangouts.', epilog="Copyright© 2016 Jorge Hortelano")
	
	#Exclusive options (different executions available)
	group = parser.add_mutually_exclusive_group()
	group.add_argument('--echo-server', '-e', action='store_true', help='Enables echo server for testing communications.')
	group.add_argument('--test-alert', '-t', action='store_true', help='Sends a simple predefined text message to the hangouts conversation.')

	args = parser.parse_args()
	
	if (args.echo_server):
		global _echo_server
		_echo_server = True
		
	if (args.test_alert):
		global _test_alert
		_test_alert = True
		

#Execute as standard main like C++
if __name__ == '__main__':
	main()
