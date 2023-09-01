
import json
from twilio.rest import Client
from modules.messaging.message_sender_interface import MessageSenderInterface

class TwilioSMSSender(MessageSenderInterface):
    def __init__(self, credentials_file_path):
        self.credentials_file_path = credentials_file_path

    def get_credentials(self):
        with open(self.credentials_file_path, "r") as config_file:
            config = json.load(config_file)
        return config
    def send_sms(self, recipient, message):
        try:
            credentials = self.get_credentials()

            client = Client(credentials["twilio_sid"], credentials["twilio_token"])
            # Use the Twilio API to send SMS messages
            client.messages.create(
                to=recipient,
                from_=credentials["from_phone_number"],
                body=message
            )
            return True  # Message sent successfully
        except Exception as e:
            print(f"Failed to send SMS: {str(e)}")
            return False  # Message sending failed
