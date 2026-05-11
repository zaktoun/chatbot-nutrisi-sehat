import google.generativeai as genai
import logging
from typing import Tuple
from datetime import datetime
from config import Config

# Setup logging
logger = logging.getLogger(__name__)


class NutrisiChatbot:
    """
    Chatbot nutrisi berbasis Google Gemini dengan error handling robust.
    
    Fitur:
    - Respons berdasarkan AI generatif Gemini
    - Error handling komprehensif
    - Logging untuk debugging
    - Timeout protection
    """
    
    SYSTEM_PROMPT = """Anda adalah ahli nutrisi profesional yang membantu pengguna memahami kebutuhan gizi, 
rekomendasi makanan sehat, dan pola makan seimbang. Berikan jawaban yang:
1. Akurat dan berbasis sains
2. Mudah dipahami oleh awam
3. Praktis dan bisa langsung diaplikasikan
4. Menyebutkan sumber atau referensi jika relevan

Jika pertanyaan di luar topik nutrisi, tetap membantu tetapi arahkan ke topik nutrisi jika memungkinkan."""
    
    def __init__(self):
        """Inisialisasi chatbot dengan validasi dan konfigurasi API."""
        try:
            # Validasi konfigurasi
            Config.validate()
            Config.log_config()
            
            # Konfigurasi Gemini API
            genai.configure(api_key=Config.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(
                model_name=Config.get_model(),
                generation_config=Config.get_generation_config(),
                system_instruction=self.SYSTEM_PROMPT
            )
            
            logger.info(f"✅ Chatbot berhasil diinisialisasi dengan model {Config.get_model()}")
        
        except ValueError as e:
            logger.error(f"❌ Error konfigurasi: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"❌ Error saat inisialisasi chatbot: {str(e)}")
            raise
    
    def tanya(self, pertanyaan: str) -> Tuple[str, bool]:
        """
        Mengirim pertanyaan ke model Gemini dan mengembalikan jawaban.
        
        Args:
            pertanyaan (str): Pertanyaan dari pengguna
        
        Returns:
            Tuple[str, bool]: (jawaban, is_success)
                - jawaban: Teks respons dari AI atau pesan error
                - is_success: True jika berhasil, False jika ada error
        """
        # Validasi input
        if not pertanyaan or not pertanyaan.strip():
            msg = "⚠️ Silakan masukkan pertanyaan tentang nutrisi terlebih dahulu."
            logger.warning(msg)
            return msg, False
        
        pertanyaan = pertanyaan.strip()
        
        # Validasi panjang input
        if len(pertanyaan) > 2000:
            msg = "❌ Pertanyaan terlalu panjang (max 2000 karakter). Silakan ringkas."
            logger.warning(msg)
            return msg, False
        
        try:
            logger.info(f"📝 Memproses pertanyaan: {pertanyaan[:100]}...")
            
            # Generate respons dengan timeout
            response = self.model.generate_content(
                pertanyaan,
                request_options={"timeout": Config.CHAT_TIMEOUT}
            )
            
            # Validasi respons
            if not response or not response.text:
                msg = "⚠️ Model tidak menghasilkan respons. Coba lagi dengan pertanyaan berbeda."
                logger.warning(msg)
                return msg, False
            
            jawaban = response.text.strip()
            logger.info(f"✅ Jawaban berhasil dihasilkan ({len(jawaban)} karakter)")
            return jawaban, True
        
        except Exception as e:
            error_str = str(e).lower()
            
            # Handle berbagai tipe error dengan pesan yang spesifik
            if "blocked" in error_str or "safety" in error_str:
                msg = "❌ Pertanyaan Anda tidak bisa diproses karena melanggar kebijakan keamanan."
            elif "timeout" in error_str or "deadline" in error_str:
                msg = f"⏱️ Waktu tunggu habis ({Config.CHAT_TIMEOUT}s). Silakan coba lagi."
            elif "connection" in error_str or "network" in error_str:
                msg = f"🌐 Error koneksi API: Periksa internet Anda dan coba lagi."
            elif "quota" in error_str or "resource_exhausted" in error_str:
                msg = "❌ Kuota API Google Gemini habis. Silakan coba lagi nanti."
            elif "authentication" in error_str or "invalid_api_key" in error_str:
                msg = "❌ Error autentikasi: API Key tidak valid atau sudah kedaluwarsa."
            else:
                msg = f"❌ Error: {str(e)[:100]}"
            
            logger.error(f"Error saat memproses pertanyaan: {type(e).__name__}: {str(e)}")
            return msg, False
    
    @staticmethod
    def format_timestamp() -> str:
        """Dapatkan timestamp saat ini dalam format yang readable."""
        return datetime.now().strftime("%H:%M:%S")
    
    @staticmethod
    def get_info() -> dict:
        """Dapatkan informasi tentang chatbot."""
        return {
            "nama": "Chatbot Nutrisi Sehat",
            "model": Config.get_model(),
            "versi": "2.0.0",
            "pengembang": "Ahmad Sani / Hacktiv8",
        }
