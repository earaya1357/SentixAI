import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory
import PIL, os
import pandas as pd
from dotenv import load_dotenv 


load_dotenv()
pword = os.getenv('KEY2')
genai.configure(api_key=pword)

config = {
    'temperature': 0.9,
    'top_p': 0.9,
    'top_k': 1,
    'max_output_tokens': 3000,
    'response_mime_type': 'text/plain',
}


safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    }

model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                              generation_config=config,
                              safety_settings=safety_settings,
                                system_instruction="Perform sentiment analysis on incoming texts for products. Provide the strength level of each sentiment score. Provide the output as in a json format as sentiment: score, strength: score (with number), vader_score: score, explanation: text, tasks: potential tasks to improve the sentiment",
)

multimodel = genai.GenerativeModel(model_name='gemini-1.5-flash',
                              generation_config=config,
                                system_instruction="Analyze the overall history of the data provided with sentiment analysis, strength, vader score (-4 to 4), explanation, and tasks to improve the score based on overall information.",#. Perform sentiment analysis on incoming texts for a product. Provide the output as in a single json format as explanation: text, tasks: potential tasks to improve the sentiment",
)

def overviewanalysis(question: list)->str:
    chat = multimodel.start_chat(history=[])
    response = chat.send_message(question)
    return response.text

def askgemini(question: str):
    chat = model.start_chat()
    response = chat.send_message(question, stream=False)
    return response.text



