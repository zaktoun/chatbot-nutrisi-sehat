🥦 Chatbot Nutrisi Sehat
💡 Deskripsi Proyek

Chatbot Nutrisi Sehat adalah aplikasi berbasis web menggunakan Streamlit dan Google Gemini API yang membantu pengguna memahami kebutuhan gizi harian, rekomendasi makanan sehat, serta perbandingan nilai nutrisi berbagai bahan makanan.
Aplikasi ini dikembangkan sebagai Proyek Akhir Hacktiv8 untuk mengimplementasikan kemampuan integrasi AI dan antarmuka pengguna interaktif.

🎯 Tujuan Proyek

Membantu pengguna mendapatkan informasi nutrisi dengan cepat dan akurat.

Menunjukkan penerapan Natural Language Processing (NLP) menggunakan model Gemini (LLM).

Membuat chatbot AI yang dapat memahami konteks dan memberikan rekomendasi gizi yang relevan.

⚙️ Fitur Utama

✅ Tanya jawab seputar nutrisi, gizi seimbang, dan pola makan sehat.
✅ Menggunakan model AI Gemini 2.5 Flash dari Google Generative AI.
✅ Antarmuka interaktif menggunakan Streamlit.
✅ Dukungan .env untuk keamanan API Key.
✅ Dapat di-deploy ke platform seperti Streamlit Cloud atau Hugging Face Spaces.

🧠 Model AI yang Digunakan

Model: gemini-2.5-flash

API: Google Generative AI (Gemini)

Peran AI:
Model bertugas memahami pertanyaan pengguna, menganalisis konteks, dan menghasilkan jawaban deskriptif tentang nutrisi, termasuk fungsi zat gizi, manfaat makanan, dan rekomendasi pola makan sehat berdasarkan pertanyaan pengguna.

🧩 Arsitektur Proyek
📂 Final Projek Hacktiv8/
│
├── app.py                # Main Streamlit app
├── chatbot_nutrisi.py    # Modul logika chatbot (interaksi AI)
├── config.py             # Konfigurasi API dan model
├── requirements.txt      # Daftar dependensi Python
├── .env.example          # Template API Key
└── README.md             # Dokumentasi proyek

🔧 Instalasi dan Konfigurasi
1️⃣ Clone repository
git clone https://github.com/username/chatbot-nutrisi.git
cd chatbot-nutrisi

2️⃣ Buat virtual environment
python -m venv myenv
source myenv/bin/activate     # (Ubuntu / Mac)
myenv\Scripts\activate        # (Windows)

3️⃣ Install dependensi
pip install -r requirements.txt

4️⃣ Siapkan file .env

Buat file bernama .env di folder utama, lalu isi dengan:

GOOGLE_API_KEY=YOUR_API_KEY_HERE


Catatan: API key bisa diperoleh dari
🔗 https://makersuite.google.com/app/apikey

5️⃣ Jalankan aplikasi
streamlit run app.py


Akses di browser melalui URL lokal (biasanya):
👉 http://localhost:8501

🧾 Contoh Penggunaan

Masukkan pertanyaan seperti:

“Apa saja nutrisi penting untuk anak?”

“Bandingkan nilai gizi pisang dan lemon.”

“Makanan yang tinggi protein tapi rendah lemak apa saja?”

Contoh output:

Nutrisi harian yang tepat sangat penting untuk pertumbuhan anak. Gizi seimbang terdiri dari karbohidrat kompleks, protein, lemak sehat, vitamin, dan mineral...

🖼️ Tampilan Antarmuka

(Ganti dengan screenshot asli chatbot kamu seperti yang kamu tampilkan di Streamlit.)

🔐 Keamanan

File .env tidak boleh di-upload ke GitHub.

Tambahkan file .gitignore:

.env
__pycache__/
myenv/


Jangan pernah menampilkan API Key di terminal atau log.

🧰 Teknologi yang Digunakan
Komponen	Deskripsi
Python 3.12+	Bahasa utama
Streamlit	Framework UI
Google Generative AI (Gemini)	Model AI
dotenv	Manajemen variabel lingkungan
LangChain (opsional)	Integrasi AI modular
📚 Dokumentasi Tambahan

Google Generative AI Python SDK

Streamlit Docs

Hacktiv8 Data Science Program

👨‍💻 Kontributor

Nama: Ahmad Sani
Program: Hacktiv8 Data Science / Final Project
Tahun: 2025

📜 Lisensi

MIT License © 2025 Ahmad Sani
Diperbolehkan digunakan untuk tujuan pembelajaran dan publikasi oleh Hacktiv8.

🚀 Status Proyek

✅ Selesai — berjalan dengan model Gemini 2.5 Flash tanpa error.
📍 Siap untuk publikasi dan penilaian proyek akhir Hacktiv8.