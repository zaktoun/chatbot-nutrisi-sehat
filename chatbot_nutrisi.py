import google.generativeai as genai
from config import Config


class NutrisiChatbot:
    """Chatbot nutrisi sederhana berbasis Google Gemini."""

    def __init__(self):
        if not Config.GOOGLE_API_KEY:
            raise ValueError("❌ GOOGLE_API_KEY belum diatur di file .env")

        # Konfigurasi Gemini
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(Config.get_model())

    def tanya(self, pertanyaan: str) -> str:
        """Mengirim pertanyaan ke model dan mengembalikan jawaban."""
        if not pertanyaan.strip():
            return "Silakan masukkan pertanyaan tentang nutrisi."

        try:
            response = self.model.generate_content(pertanyaan)
            return response.text.strip()
        except Exception as e:
            return f"Maaf, terjadi kesalahan saat memproses: {str(e)}"

