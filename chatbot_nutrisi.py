import google.generativeai as genai
import logging
from typing import Optional
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
    
    def tanya(self, pertanyaan: str) -> tuple[str, bool]:
        """
        Mengirim pertanyaan ke model Gemini dan mengembalikan jawaban.
        
        Args:
            pertanyaan (str): Pertanyaan dari pengguna
        
        Returns:
            tuple[str, bool]: (jawaban, is_success)
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
        
        except google.generativeai.types.BlockedPromptException:
            msg = "❌ Pertanyaan Anda tidak bisa diproses karena melanggar kebijakan keamanan."
            logger.error(msg)
            return msg, False
        
        except TimeoutError:
            msg = f"⏱️ Waktu tunggu habis ({Config.CHAT_TIMEOUT}s). Silakan coba lagi."
            logger.error(msg)
            return msg, False
        
        except google.generativeai.types.APIConnectionError as e:
            msg = f"🌐 Error koneksi API: Periksa internet Anda dan coba lagi. ({str(e)[:50]})"
            logger.error(f"API Connection Error: {str(e)}")
            return msg, False
        
        except google.generativeai.types.APIStatusError as e:
            if "quota" in str(e).lower():
                msg = "❌ Kuota API Google Gemini habis. Silakan coba lagi nanti."
            else:
                msg = f"❌ Error API: {str(e)[:100]}"
            logger.error(f"API Status Error: {str(e)}")
            return msg, False
        
        except Exception as e:
            msg = f"❌ Error tidak terduga: {str(e)[:100]}"
            logger.error(f"Unexpected Error: {type(e).__name__}: {str(e)}")
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
