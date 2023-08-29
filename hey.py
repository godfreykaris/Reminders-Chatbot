import requests

# Define the URL of your Flask application
url = "/api/send_message"  # Update the URL as needed

# Define the data to be sent in the request's JSON body
data = {
    "recipient": "+254759741544",  # Replace with the recipient's phone number
    "message": "Hello, this is a test message from bigs",  # Replace with your message
    "type": "whatsapp"  # Specify the message type (sms or whatsapp)
}

# Send an HTTP POST request to the /api/send_message route
response = requests.post(url, json=data)

# Print the response from the server
print(response.status_code)  # Print the HTTP status code
print(response.json())  # Print the JSON response from the server






