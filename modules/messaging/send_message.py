
import json

from modules.messaging.sms_sender import TwilioSMSSender
from modules.messaging.whatsapp_sender import TwilioWhatsAppSender


class MessageSender:
    def send_message(self, recipient, message, message_type):
        
        if not recipient or not message or not message_type:
            return json.dumps({'message': 'Invalid input data'}), 400

        try:
            if message_type == 'sms':
                message_sender = TwilioSMSSender("config.json")
                sent = message_sender.send_sms(recipient, message)
            elif message_type == 'whatsapp':
                message_sender = TwilioWhatsAppSender("config.json")
                sent = message_sender.send_whatsapp(recipient, message)
            else:
                return json.dumps({'message': 'Invalid message type'}), 400

            if sent:
                return json.dumps({'message': f'{message_type.capitalize()} sent successfully'})
            else:
                #return json.dumps({'message': f'Failed to send {message_type}'}), 500
                # For testing only
                return json.dumps({'message': sent}), 500

    
        except Exception as e:
            # return json.dumps({'message': f'Failed to send {message_type}', 'error': str(e)}), 500
            
            # For testing only
            return json.dumps({'message': str(e), 'error': str(e)}), 500