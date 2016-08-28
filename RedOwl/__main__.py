import os
import messaging.alert_client

def main():
	"""Main entry point."""
	print("RedOwl starting....")
	
	#Send test alert
	messaging.alert_client.send_alert('Test message')
	
	#message_service.connect_to_hangouts()
	print("RedOwl closing....")

#Execute as standard main like C++
if __name__ == '__main__':
	main()
