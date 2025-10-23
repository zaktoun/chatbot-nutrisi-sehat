import streamlit as st
from chatbot_nutrisi import NutrisiChatbot

# Judul aplikasi
st.set_page_config(page_title="💬 Chatbot Nutrisi", page_icon="🥦")

st.title("🥦 Chatbot Nutrisi Sehat")
st.write("Tanyakan apa saja tentang gizi, makanan sehat, dan nutrisi tubuh.")

# Inisialisasi chatbot
if "bot" not in st.session_state:
    st.session_state.bot = NutrisiChatbot()

# Input pengguna
pertanyaan = st.text_area("Masukkan pertanyaan Anda:", placeholder="Contoh: Apa manfaat protein untuk tubuh?")

if st.button("Tanyakan"):
    with st.spinner("Sedang berpikir... 🍎"):
        jawaban = st.session_state.bot.tanya(pertanyaan)
        st.success(jawaban)

