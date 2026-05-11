import os
import logging
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Muat file .env
load_dotenv()


class Config:
    """Konfigurasi aplikasi Chatbot Nutrisi Sehat."""
    
    # API Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Model Configuration
    MODEL = os.getenv("MODEL", "gemini-2.5-flash")
    TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 1024))
    TOP_P = float(os.getenv("TOP_P", 0.95))
    
    # Application Configuration
    APP_TITLE = "🥦 Chatbot Nutrisi Sehat"
    APP_ICON = "🥦"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Chat Configuration
    MAX_CHAT_HISTORY = int(os.getenv("MAX_CHAT_HISTORY", 50))
    CHAT_TIMEOUT = int(os.getenv("CHAT_TIMEOUT", 30))  # seconds
    
    @staticmethod
    def validate():
        """Validasi konfigurasi aplikasi."""
        if not Config.GOOGLE_API_KEY:
            logger.error("❌ GOOGLE_API_KEY tidak ditemukan di file .env")
            raise ValueError(
                "GOOGLE_API_KEY belum diatur. "
                "Silakan copy .env.example ke .env dan isi dengan API Key Anda."
            )
        
        if Config.TEMPERATURE < 0 or Config.TEMPERATURE > 2:
            logger.warning(f"⚠️ TEMPERATURE={Config.TEMPERATURE} mungkin tidak optimal")
        
        if Config.MAX_TOKENS < 100:
            logger.warning(f"⚠️ MAX_TOKENS={Config.MAX_TOKENS} terlalu kecil")
        
        logger.info("✅ Konfigurasi valid dan siap digunakan")
    
    @staticmethod
    def get_model():
        """Dapatkan nama model AI yang digunakan."""
        return Config.MODEL
    
    @staticmethod
    def get_generation_config():
        """Dapatkan konfigurasi generation untuk Gemini API."""
        return {
            "temperature": Config.TEMPERATURE,
            "top_p": Config.TOP_P,
            "max_output_tokens": Config.MAX_TOKENS,
        }
    
    @staticmethod
    def log_config():
        """Log konfigurasi (tanpa menampilkan API Key)."""
        config_info = {
            "Model": Config.MODEL,
            "Temperature": Config.TEMPERATURE,
            "Max Tokens": Config.MAX_TOKENS,
            "Top P": Config.TOP_P,
            "Chat Timeout": f"{Config.CHAT_TIMEOUT}s",
            "Debug Mode": Config.DEBUG,
        }
        logger.info("📋 Konfigurasi Aplikasi:")
        for key, value in config_info.items():
            logger.info(f"   {key}: {value}")
