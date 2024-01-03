from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
atlas_username = os.getenv("ATLAS_USERNAME")
atlas_password = os.getenv("ATLAS_PASSWORD")