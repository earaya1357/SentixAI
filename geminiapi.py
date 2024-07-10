import PIL.Image
import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory
import PIL


with open('geminikey.txt', 'r') as k:
    key = k.readlines()
genai.configure(api_key=key[0])

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

def askgemini(question: str):
    chat = model.start_chat()
    response = chat.send_message(question, stream=False)
    return response.text



