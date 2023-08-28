
from flask import jsonify, request

from modules.messaging.sms_sender import TwilioSMSSender
from modules.messaging.whatsapp_sender import TwilioWhatsAppSender


class MessageSender:
    def send_message(self):
        data = request.get_json()
        recipient = data.get('recipient')
        message = data.get('message')
        message_type = data.get('type')  # 'sms' or 'whatsapp'

        if not recipient or not message or not message_type:
            return jsonify({'message': 'Invalid input data'}), 400

        try:
            if message_type == 'sms':
                message_sender = TwilioSMSSender("config.json")
                sent = message_sender.send_sms(recipient, message)
            elif message_type == 'whatsapp':
                message_sender = TwilioWhatsAppSender("config.json")
                sent = message_sender.send_whatsapp(recipient, message)
            else:
                return jsonify({'message': 'Invalid message type'}), 400

            if sent:
                return jsonify({'message': f'{message_type.capitalize()} sent successfully'})
            else:
                #return jsonify({'message': f'Failed to send {message_type}'}), 500
                # For testing only
                return jsonify({'message': sent}), 500

    
        except Exception as e:
            # return jsonify({'message': f'Failed to send {message_type}', 'error': str(e)}), 500
            
            # For testing only
            return jsonify({'message': str(e), 'error': str(e)}), 500