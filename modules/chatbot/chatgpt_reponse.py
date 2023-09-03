import json
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


            return json.dumps({'message': 'Response generated successfully', 'bot_response': bot_response})

        except Exception as e:
            #return json.dumps({'message': 'Error generating chatgpt response', 'error': str(e)}), 500
            return json.dumps({'message': str(e), 'error': str(e)}), 500 # For testing only

    def generate_user_message(self, prompt_message, response_max_tokens):
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
        
    
    def chat_with_user(self, user_input, response_max_tokens):
        credentials = self.get_credentials()

        try:
            openai.api_key = credentials['openai_key']

            # Combine the user's input with a chat prompt
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                  messages=[                    
                    {
                        "role": "user",
                        "content": user_input + "."
                    },
                    {
    "role": "system",
    "content": "Your role is to review user-generated reports. Use NLP to understand the user's response and trigger the closest matching option based on their input. Choose only one option:\n\n"
                   "1. When the user reports progress, success, or failure in relation to their goal, prompt them to share details about their journey. Encourage them to provide insights, describe challenges faced, and outline the specific steps they took to reach or not reach the goal."
                   "2. If the user's response indicates a positive experience (e.g., 'It was nice,' 'I felt good,' 'I had a nice experience,' 'I enjoyed it,' 'I had a great time,' 'It was fantastic,' 'I had a blast,' 'I enjoyed it thoroughly,' 'It was an amazing experience,' 'I felt really good,' 'It was awesome,' 'I had a wonderful time,' 'I loved it,' 'It was a pleasant experience,' 'I felt happy,' 'It was fantastic!' 'I had a fantastic day,' 'I had so much fun,' 'I had a really good time,' 'It was a fantastic experience,' 'I felt great during it,' 'It was superb,' 'I had an excellent time,' 'I had an enjoyable experience,' 'I felt satisfied,' 'It was a fantastic outing,' 'I had a terrific time,' 'It was a wonderful experience,' 'I felt joyful,' 'It was marvelous,' 'I had a marvelous experience,' 'I felt fantastic,' 'It was top-notch,' 'I had a top-notch experience,' 'I had a splendid time,' 'It was exceptional,' 'I had an extraordinary experience,' 'I felt on top of the world,' 'It was phenomenal,' 'I had a phenomenal experience,' 'I felt ecstatic,' 'It was mind-blowing,' 'I had a mind-blowing experience,' 'I felt euphoric,' 'It was breathtaking,' 'I had a breathtaking experience,' 'I felt elated,' 'It was outstanding,' 'I had an outstanding experience,' 'I felt overjoyed,' 'It was remarkable,' 'I had a remarkable experience,' 'I felt thrilled,' 'It was terrific,' 'I had a terrific experience,' 'I felt delighted,' 'It was exceptional,' 'I had an exceptional experience,' 'I felt jubilant,' 'It was incredible,' 'I had an incredible experience,' 'I felt euphoric,' 'It was extraordinary,' 'I had an extraordinary experience), respond with 'Okay.' without additional prompts\n"                
                   "3. If the user's response indicates a negative experience (e.g., 'I had a terrible time,' 'It was awful,' 'I had a dreadful experience,' 'I felt miserable,' 'It was horrible,' 'I had a horrible experience,' 'I felt terrible,' 'It was terrible,' 'I had a terrible experience,' 'I had an awful time,' 'It was dreadful,' 'I had a dreadful time,' 'I felt wretched,' 'It was dreadful,' 'I had a dreadful experience,' 'I felt awful,' 'It was horrendous,' 'I had a horrendous time,' 'I felt horrific,' 'It was horrific,' 'I had a horrific experience,' 'I felt dreadful,' 'It was nightmarish,' 'I had a nightmarish time,' 'I felt nightmarish,' 'It was nightmarish,' 'I had a nightmarish experience,' 'I felt horrendous,' 'It was disastrous,' 'I had a disastrous time,' 'I felt disastrous,' 'It was disastrous,' 'I had a disastrous experience,' 'I felt catastrophic,' 'It was catastrophic,' 'I had a catastrophic time,' 'I felt catastrophic,' 'It was catastrophic,' 'I had a catastrophic experience'), respond with 'Okay.'"
                   "4. If the report provides a valid reason for not achieving the goal (e.g., 'I was in a meeting,' 'I had a doctor's appointment,' 'I was traveling for work,' 'I had a family emergency,' 'I was attending a conference,' 'I was on vacation,' 'I was working on another project,' 'I was sick and couldn't work on it,' 'I had technical difficulties,' 'I ran out of time,' 'I had a personal commitment,' 'I had a prior engagement,' 'I was caught up in unexpected tasks,' 'I faced an unforeseen obstacle,' 'I encountered an urgent matter,' 'I got sidetracked by other responsibilities,' 'I had a sudden deadline,' 'I had to handle an emergency situation,' 'I was occupied with a critical issue'), respond with 'Okay.'\n"
                   "5. If the user mentions that they did not achieve their goal, respond by asking for specific details about why they were unable to achieve it. Encourage them to share the reasons or obstacles that prevented them from reaching their goal.\n"
                   
                   
                   "Always prioritize the user's goal.\n"
                   "Always prompt for clarification when necessary.\n"
                   "Respond with 'Okay' after clarification.\n"
                   "Do not answer questions; maintain focus on the user's goal.\n"
                   "Always repond with something."
}


                    ],
                max_tokens=response_max_tokens,
                temperature=0,
            )

            # Extract the generated response from ChatGPT
            bot_response = response['choices'][0]['message']['content']

            return json.dumps({'message': 'Chat message generated successfully', 'bot_response': bot_response})

        except Exception as e:
            return json.dumps({'message': str(e), 'error': str(e)})


