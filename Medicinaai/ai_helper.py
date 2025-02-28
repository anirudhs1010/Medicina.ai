import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'),
                transport="rest",
                client_options={"api_endpoint": "generativelanguage.googleapis.com"})

def get_chatbot_response(message):
    try:
        # Create a Gemini model instance
        model = genai.GenerativeModel('gemini-pro')

        # Create a chat instance with the system prompt
        chat = model.start_chat(history=[
            {
                "role": "user",
                "parts": ["You are a helpful medical assistant. Provide accurate but cautious medical information. Always advise consulting healthcare professionals for specific medical advice."]
            },
            {
                "role": "model",
                "parts": ["I understand. I will act as a medical assistant, providing general health information while emphasizing the importance of consulting healthcare professionals for specific medical advice."]
            }
        ])

        # Get response from the model
        response = chat.send_message(message)
        return response.text

    except Exception as e:
        return f"I apologize, but I'm unable to process your request at the moment. Please try again later. Error: {str(e)}"