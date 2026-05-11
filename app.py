import streamlit as st
import logging
from chatbot_nutrisi import NutrisiChatbot
from config import Config
from datetime import datetime

# ============================================================================
# KONFIGURASI STREAMLIT
# ============================================================================

st.set_page_config(
    page_title=Config.APP_TITLE,
    page_icon=Config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# CUSTOM CSS UNTUK UI YANG LEBIH BAIK
# ============================================================================

st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 1rem 2rem;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        gap: 1rem;
    }
    
    .chat-user {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .chat-bot {
        background-color: #f1f8e9;
        border-left: 4px solid #4caf50;
    }
    
    .chat-error {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
    }
    
    /* Title styling */
    h1 {
        color: #2e7d32;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    h2 {
        color: #388e3c;
        border-bottom: 2px solid #4caf50;
        padding-bottom: 0.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #4caf50;
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "chatbot" not in st.session_state:
    try:
        st.session_state.chatbot = NutrisiChatbot()
        st.session_state.chat_history = []
        st.session_state.session_start = datetime.now()
        logger.info("✅ Chatbot berhasil diinisialisasi dalam session")
    except Exception as e:
        st.error(f"❌ Error saat menginisialisasi chatbot: {str(e)}")
        st.info("💡 **Solusi:**\n1. Pastikan file `.env` ada di folder root\n2. Isi `GOOGLE_API_KEY` dengan API key Anda\n3. Refresh halaman ini")
        st.stop()

if "show_history" not in st.session_state:
    st.session_state.show_history = True

# ============================================================================
# SIDEBAR - NAVIGATION & INFO
# ============================================================================

with st.sidebar:
    st.markdown("## ⚙️ Menu")
    
    # Tab navigation
    sidebar_tab = st.radio(
        "Pilih Menu:",
        ["💬 Chat", "📊 Info", "🔧 Pengaturan"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Info Section
    st.markdown("### 📋 Informasi Aplikasi")
    info = st.session_state.chatbot.get_info()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Model", info["model"])
        st.metric("Versi", info["versi"])
    with col2:
        st.metric("Status", "✅ Aktif")
        st.metric("Sesi", st.session_state.session_start.strftime("%H:%M:%S"))
    
    st.divider()
    
    # History Controls
    st.markdown("### 📝 Riwayat Chat")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("🗑️ Hapus Semua", use_container_width=True):
            st.session_state.chat_history = []
            st.success("✅ Riwayat chat telah dihapus")
            st.rerun()
    
    st.info(f"📊 Total pertanyaan: {len(st.session_state.chat_history)}")
    
    st.divider()
    
    # Footer
    st.markdown("""
    ---
    **Chatbot Nutrisi Sehat v2.0**
    
    Dikembangkan untuk Hacktiv8 Data Science Program
    
    📧 Pertanyaan? Hubungi developer
    """)

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================

if sidebar_tab == "💬 Chat":
    st.title("🥦 Chatbot Nutrisi Sehat")
    st.write("🎯 Tanyakan apa saja tentang gizi, makanan sehat, dan nutrisi tubuh!")
    
    # Chat display area
    st.markdown("### 💬 Percakapan")
    
    if st.session_state.chat_history:
        # Display chat history
        for idx, chat in enumerate(st.session_state.chat_history):
            # User message
            st.markdown(f"""
            <div class="chat-message chat-user">
                <div>
                    <strong>👤 Anda ({chat['timestamp']}):</strong><br/>
                    {chat['question']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Bot response
            if chat['success']:
                st.markdown(f"""
                <div class="chat-message chat-bot">
                    <div>
                        <strong>🤖 Chatbot:</strong><br/>
                        {chat['answer']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message chat-error">
                    <div>
                        <strong>⚠️ Error:</strong><br/>
                        {chat['answer']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
    else:
        st.info("💭 Belum ada percakapan. Mulai dengan mengajukan pertanyaan!")
    
    # Input section
    st.markdown("### ✍️ Ajukan Pertanyaan")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        pertanyaan = st.text_area(
            "Masukkan pertanyaan Anda:",
            placeholder="Contoh: Apa manfaat protein untuk tubuh? Berapa kebutuhan kalori harian saya?",
            height=100,
            label_visibility="collapsed"
        )
    
    with col2:
        st.write("")  # Spacing
        tombol_tanya = st.button(
            "🚀 Tanyakan",
            use_container_width=True,
            key="btn_tanya"
        )
    
    # Process user input
    if tombol_tanya:
        if not pertanyaan.strip():
            st.error("❌ Silakan masukkan pertanyaan terlebih dahulu!")
        else:
            with st.spinner("⏳ Sedang berpikir... 🍎"):
                try:
                    jawaban, is_success = st.session_state.chatbot.tanya(pertanyaan)
                    
                    # Store in history
                    chat_entry = {
                        "question": pertanyaan,
                        "answer": jawaban,
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "success": is_success
                    }
                    st.session_state.chat_history.append(chat_entry)
                    
                    # Limit history to prevent memory issues
                    if len(st.session_state.chat_history) > Config.MAX_CHAT_HISTORY:
                        st.session_state.chat_history = st.session_state.chat_history[-Config.MAX_CHAT_HISTORY:]
                    
                    st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    logger.error(f"Unexpected error: {str(e)}")

# ============================================================================
# INFO TAB
# ============================================================================

elif sidebar_tab == "📊 Info":
    st.title("📊 Informasi Aplikasi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Tentang Aplikasi")
        st.write("""
        **Chatbot Nutrisi Sehat** adalah asisten AI yang membantu Anda:
        - 🥗 Memahami kebutuhan gizi harian
        - 🍎 Mendapatkan rekomendasi makanan sehat
        - 📊 Membandingkan nilai gizi berbagai makanan
        - 💪 Merencanakan pola makan seimbang
        """)
    
    with col2:
        st.markdown("### 🔧 Teknologi")
        st.write("""
        - **AI Model:** Google Gemini 2.5 Flash
        - **Framework:** Streamlit
        - **Language:** Python 3.12+
        - **API:** Google Generative AI
        """)
    
    st.divider()
    
    st.markdown("### 📚 Contoh Pertanyaan")
    st.write("""
    1. **"Apa saja nutrisi penting untuk anak?"**
    2. **"Bandingkan nilai gizi pisang dan lemon."**
    3. **"Makanan yang tinggi protein tapi rendah lemak apa saja?"**
    4. **"Berapa kebutuhan kalori per hari untuk orang dewasa?"**
    5. **"Bagaimana cara menjalankan diet sehat yang berkelanjutan?"**
    """)
    
    st.divider()
    
    st.markdown("### 👨‍💻 Pengembang")
    st.write("""
    - **Nama:** Ahmad Sani
    - **Program:** Hacktiv8 Data Science
    - **Tahun:** 2025
    - **Versi:** 2.0.0
    """)

# ============================================================================
# SETTINGS TAB
# ============================================================================

elif sidebar_tab == "🔧 Pengaturan":
    st.title("⚙️ Pengaturan Aplikasi")
    
    st.markdown("### 🤖 Konfigurasi Model AI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Model", Config.get_model())
        st.metric("Temperature", Config.TEMPERATURE)
    
    with col2:
        st.metric("Max Tokens", Config.MAX_TOKENS)
        st.metric("Timeout (s)", Config.CHAT_TIMEOUT)
    
    st.divider()
    
    st.markdown("### 📊 Statistik Session")
    st.write(f"**Total Chat:** {len(st.session_state.chat_history)}")
    st.write(f"**Waktu Mulai:** {st.session_state.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
    st.write(f"**Durasi:** {(datetime.now() - st.session_state.session_start).total_seconds() / 60:.1f} menit")
    
    st.divider()
    
    st.markdown("### 🔐 Keamanan")
    with st.expander("ℹ️ Informasi Keamanan"):
        st.write("""
        - ✅ API Key disimpan di file `.env` (tidak di upload ke GitHub)
        - ✅ Tidak ada data sensitif yang tercatat
        - ✅ Setiap sesi bersifat independent
        - ✅ Chat history hanya tersimpan di memory session
        """)
    
    st.divider()
    
    st.markdown("### 🚀 Informasi Lainnya")
    st.write("""
    - **Framework:** Streamlit 1.28.1
    - **Python Version:** 3.12+
    - **Status:** ✅ Production Ready
    """)
