import google.generativeai as genai
import PIL.Image
import os
from dotenv import load_dotenv


load_dotenv()  # Charge les variables d'environnement du fichier .env
api_key = os.getenv("API_KEY")

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
genai.configure(api_key=os.environ["api_key"])
#img = PIL.Image.open('.\CC.png')

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
def generate(request_generate):
    response = model.generate_content([request_generate])
    #print(response.text)
    generated_text = response.candidates[0].content.parts[0].text
    return generated_text
