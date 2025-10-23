import os
from dotenv import load_dotenv

# Muat file .env
load_dotenv()

class Config:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # Model Google Gemini
    MODEL = "gemini-2.5-flash"
    TEMPERATURE = 0.6
    MAX_TOKENS = 500

    @staticmethod
    def get_model():
        return Config.MODEL

