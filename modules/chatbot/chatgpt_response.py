import json
import openai

from datetime import datetime, timedelta

class ChatGPTResponse:
    def __init__(self, credentials_file_path=None, credentials=None):
         self.credentials_file_path = credentials_file_path
         self.credentials = credentials
        
    def get_credentials(self):
        with open(self.credentials_file_path, "r") as config_file:
            config = json.load(config_file)
        return config
    
    def generate_analysis_report(self, prompt_message, response_max_tokens):
        if self.credentials:
            credentials = self.credentials
        else:
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


            return json.dumps({'message': 'Response generated successfully', 'bot_response': bot_response})

        except Exception as e:
            #return json.dumps({'message': 'Error generating chatgpt response', 'error': str(e)}), 500
            return json.dumps({'message': str(e), 'error': str(e)}), 500 # For testing only

    def generate_user_message(self, prompt_message, response_max_tokens):
        if self.credentials:
            credentials = self.credentials
        else:
            credentials = self.get_credentials()

        try:
            openai.api_key = credentials['openai_key']

            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                  messages=[
                     {
                       "role": "system",
                       "content": prompt_message,
                     },
                     ],
                temperature=1,
                max_tokens=response_max_tokens,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Extract the generated response from ChatGPT
            bot_response = response['choices'][0]['message']['content']

            return json.dumps({'message': 'User message generated successfully', 'user_message': bot_response})

        except Exception as e:
            return json.dumps({'message': str(e), 'error': str(e)}), 500  # For testing only
        
    
    def chat_with_user(self, history, response_max_tokens):
        if self.credentials:
            credentials = self.credentials
        else:
            credentials = self.get_credentials()

        try:
            openai.api_key = credentials['openai_key']

            previous_history = history[:]
            systemrole = {
                            "role": "system",
                            "content": "Review user-generated reports using NLP to identify one of the following scenarios based on user input:\n\n"
                                       "1. If the user discusses progress, success, or failure related to a goal, ask for details about their experience and challenges.\n"
                                       "2. For positive experiences, respond with 'Okay.'\n"
                                       "3. For negative experiences, respond with 'Okay.'\n"
                                       "4. If the user gives a valid reason for not achieving a goal (e.g., 'I was in a meeting'), respond with 'Okay.'\n"
                                       "5. If the user states they didn't achieve their goal, ask for specific reasons why.\n"
                                       "6. If the input is unclear, inform the user and ask for clearer content. Do not answer questions; focus solely on the user's goal."
                        }
            previous_history.insert(0, systemrole)

            
            # Combine the user's input with a chat prompt
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=previous_history,
                max_tokens=response_max_tokens,
                temperature=0,
            )

            # Extract the generated response from ChatGPT
            bot_response = response['choices'][0]['message']['content']

            return json.dumps({'message': 'Chat message generated successfully', 'bot_response': bot_response, 'status': 200})

        except Exception as e:
            print(str(e))
            return json.dumps({'message': str(e), 'error': str(e), 'status': 500})

    def fetch_history_from_database(self, database_initializer, user_id, goal_id):

        try:
            database_connection = database_initializer.get_database_connection()
            cursor = database_connection.cursor()

            # Get the current date and time
            current_datetime = datetime.utcnow()

            # Format it as per your requirement
            formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S.%f%z')

            # Calculate the timestamp 10 hours ago
            ten_hours_ago = datetime.utcnow() - timedelta(hours=10)
            ten_hours_ago = ten_hours_ago.strftime('%Y-%m-%d %H:%M:%S.%f%z')

            # Update the conversation_history to NULL if history_updated_on is older than ten_hours_ago
            cursor.execute("UPDATE goals SET conversation_history = NULL, history_updated_on = %s WHERE user_id = %s AND id = %s AND (history_updated_on < %s OR history_updated_on IS NULL);", (formatted_datetime, user_id, goal_id, ten_hours_ago))

            database_connection.commit()

            # Retrieve the user's goal based on user_id and goal_id
            cursor.execute("SELECT conversation_history FROM goals WHERE user_id = %s AND id = %s;", (user_id, goal_id))
            conversation_history = cursor.fetchone()

            
            return conversation_history[0]
        except Exception as e:
            print(str(e))
            # Handle database errors or other exceptions
            return None
        finally:
            cursor.close()
            database_connection.close()
    
    def store_history_to_database(self, database_initializer, user_id, goal_id, history):
        try:
            database_connection = database_initializer.get_database_connection()
            cursor = database_connection.cursor()

            # Update the user's goal with the conversation history
            cursor.execute("UPDATE goals SET conversation_history = %s WHERE user_id = %s AND id = %s", (history, user_id, goal_id))
            database_connection.commit()

            return json.dumps({'message': 'History stored successfully', 'status': 200})
        except Exception as e:
            # Handle database errors or other exceptions
            return json.dumps({'message': str(e), 'error': str(e), 'status': 500})
        finally:
            if cursor:
                cursor.close()
            if database_connection:
                database_connection.close()


