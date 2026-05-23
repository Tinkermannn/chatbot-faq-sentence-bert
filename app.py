import streamlit as st
import time
from retrieval_engine import FAQEngine

# --- Konfigurasi Halaman Streamlit ---
# Mengatur judul tab browser, ikon, dan layout
st.set_page_config(page_title="AI FAQ Chatbot", page_icon="🤖", layout="centered")

# --- 1. Manajemen Loading Model (Caching) ---
# Menggunakan decorator @st.cache_resource agar model Transformer yang berukuran besar (~487MB)
# dan matriks data FAQ hanya dimuat SATU KALI saat server pertama kali di-run.
# Tanpa ini, Streamlit akan memuat ulang model setiap kali user mengirim pesan (OOM & lambat).
@st.cache_resource
def load_faq_engine():
    # Inisialisasi class dari retrieval_engine.py
    # Ganti string model dengan 'faq_sbert_finetuned' jika Anda ingin memakai model lokal Anda
    engine = FAQEngine(
        # model_name_or_path='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', 
        model_name_or_path='faq_sbert_finetuned',
        threshold=0.45
    )
    
    try:
        # Load dataset JSON & Numpy (menggantikan .pkl)
        engine.load_data(json_path='faq_data.json', npy_path='faq_embeddings.npy')
    except FileNotFoundError:
        # Menangani error jika user belum mengekstrak file pickle
        st.error("🚨 Error: File `faq_data.json` atau `faq_embeddings.npy` tidak ditemukan di direktori proyek!")
        st.info("Pastikan Anda sudah mengekstrak data dari file .pkl menjadi JSON & Numpy.")
        st.stop() # Hentikan eksekusi UI
        
    return engine

# Panggil fungsi cache untuk mendapatkan objek mesin
engine = load_faq_engine()


# --- 2. Manajemen State (Session State) ---
# Menyimpan riwayat percakapan di memori browser pengguna agar chat tidak hilang.
if "messages" not in st.session_state:
    # Set pesan default dari bot di awal sesi
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Saya adalah AI FAQ Chatbot Akademik. Ada yang bisa saya bantu terkait informasi kampus?"}
    ]


# --- Tampilan UI (Frontend) ---
st.title("💬 Akademik AI Chatbot")
st.caption("🚀 Didukung oleh Sentence-BERT. Tanyakan apa saja seputar regulasi dan akademik.")
st.divider()

# Loop history percakapan untuk me-render bubble chat layaknya WhatsApp
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# --- 3. Logika Antarmuka (Chat Input) ---
# st.chat_input akan menahan eksekusi di bawahnya hingga user menekan Enter
if prompt := st.chat_input("Ketik pertanyaan Anda di sini..."):
    
    # 1. Tampilkan pesan user ke layar dan simpan ke riwayat session
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # 2. Proses pencarian jawaban (Inference)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Animasi loading saat model sedang menghitung Cosine Similarity
        with st.spinner("Sedang mencari jawaban terbaik..."):
            start_time = time.time()
            
            # Panggil metode pencarian dari FAQEngine
            answer = engine.retrieve_answer(prompt)
            
            # Opsional: Beri sedikit jeda 0.5s agar UX terasa natural (tidak instan dan aneh)
            time.sleep(0.5) 
            
            inference_time = time.time() - start_time
            
        # Render teks jawaban ke layar
        message_placeholder.markdown(answer)
        # Menampilkan waktu respons (opsional, bagus untuk debugging performa)
        st.caption(f"⚡ Dijawab dalam {inference_time:.2f} detik")
        
    # 3. Simpan balasan bot ke dalam riwayat session
    st.session_state.messages.append({"role": "assistant", "content": answer})
