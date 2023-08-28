import json
from flask import jsonify
import openai

class ChatGPTResponse:
    def __init__(self, credentials_file_path):
        self.credentials_file_path = credentials_file_path
        
    def get_credentials(self):
        with open(self.credentials_file_path, "r") as config_file:
            config = json.load(config_file)
        return config
    
    def generate_analysis_report(self, prompt_message, response_max_tokens):
        credentials = self.get_credentials()

        try:
            openai.api_key = credentials['openai_key']

            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                  messages=[
                    {"role": "user", "content": prompt_message}],
                max_tokens=response_max_tokens,
                temperature=1.2,
            )

            # Extract the generated response from ChatGPT
            bot_response = response['choices'][0]['message']['content']


            return jsonify({'message': 'Response generated successfully', 'bot_response': bot_response})

        except Exception as e:
            #return jsonify({'message': 'Error generating chatgpt response', 'error': str(e)}), 500
            return jsonify({'message': str(e), 'error': str(e)}), 500 # For testing only

    def generate_user_message(self, prompt_message, response_max_tokens):
        credentials = self.get_credentials()

        try:
            openai.api_key = credentials['openai_key']

            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                  messages=[
                    {"role": "user", "content": prompt_message}],
                max_tokens=response_max_tokens,
                temperature=1.2,
            )

            # Extract the generated response from ChatGPT
            bot_response = response['choices'][0]['message']['content']

            return jsonify({'message': 'User message generated successfully', 'user_message': bot_response})

        except Exception as e:
            return jsonify({'message': str(e), 'error': str(e)}), 500  # For testing only
        
    
    def chat_with_user(self, user_input, response_max_tokens):
        credentials = self.get_credentials()

        try:
            openai.api_key = credentials['openai_key']

            # Combine the user's input with a chat prompt
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                  messages=[
                    {"role": "user", "content": user_input + "."}],
                max_tokens=193,
                temperature=0,
            )

            # Extract the generated response from ChatGPT
            bot_response = response['choices'][0]['message']['content']

            return jsonify({'message': 'Chat message generated successfully', 'bot_response': bot_response})

        except Exception as e:
            return jsonify({'message': str(e), 'error': str(e)})


