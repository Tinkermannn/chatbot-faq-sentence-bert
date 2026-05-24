import streamlit as st
import time
from retrieval_engine import FAQEngine

# --- Konfigurasi Halaman Streamlit ---
# Mengatur judul tab browser, ikon, dan layout
st.set_page_config(page_title="FAQ Akademik DTE", page_icon="🎓", layout="centered")

# =====================================================================
# CUSTOM CSS — Kosmetik UI (tidak mengubah logika apapun)
# =====================================================================
st.markdown("""
<style>
/* ---- Import Google Font ---- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ---- Root variables ---- */
:root {
    --primary: #4F46E5;
    --primary-light: #818CF8;
    --accent: #06B6D4;
    --surface: #1E1B4B;
    --surface-light: #312E81;
    --text-primary: #F8FAFC;
    --text-secondary: #CBD5E1;
    --gradient-main: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #06B6D4 100%);
    --gradient-card: linear-gradient(135deg, rgba(79,70,229,0.12) 0%, rgba(124,58,237,0.08) 100%);
}

/* ---- Global ---- */
.stApp {
    font-family: 'Inter', sans-serif !important;
}

/* ---- Header hero ---- */
.hero-container {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem 1rem;
    margin-bottom: 0.5rem;
}

.hero-icon {
    font-size: 3.2rem;
    margin-bottom: 0.5rem;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-8px); }
}

.hero-title {
    font-family: 'Inter', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818CF8 0%, #06B6D4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.35rem;
    line-height: 1.2;
}

.hero-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    color: #94A3B8;
    font-weight: 400;
    max-width: 540px;
    margin: 0 auto;
    line-height: 1.5;
}

/* ---- Badge pills ---- */
.badge-row {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.3rem 0.75rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    border: 1px solid rgba(129,140,248,0.25);
    background: rgba(79,70,229,0.1);
    color: #A5B4FC;
}

/* ---- Divider ---- */
.styled-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(129,140,248,0.35), transparent);
    border: none;
    margin: 0.75rem 0 1.25rem 0;
    border-radius: 2px;
}

/* ---- Sidebar ---- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E1B4B 0%, #0F172A 100%) !important;
    border-right: 1px solid rgba(129,140,248,0.12) !important;
}

.sidebar-header {
    text-align: center;
    padding: 1.2rem 0.5rem 0.8rem 0.5rem;
}

.sidebar-logo {
    font-size: 2.6rem;
    margin-bottom: 0.3rem;
}

.sidebar-brand {
    font-family: 'Inter', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    background: linear-gradient(90deg, #818CF8, #06B6D4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.sidebar-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(129,140,248,0.3), transparent);
    border: none;
    margin: 0.8rem 0;
}

.info-card {
    background: rgba(79,70,229,0.08);
    border: 1px solid rgba(129,140,248,0.15);
    border-radius: 12px;
    padding: 1rem 1rem;
    margin-bottom: 0.75rem;
}

.info-card-title {
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #818CF8;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.35rem;
}

.info-card-body {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: #CBD5E1;
    line-height: 1.65;
}

.member-name {
    font-weight: 600;
    color: #E2E8F0;
}

.member-nim {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    color: #64748B;
    font-weight: 500;
}

.tip-card {
    background: rgba(6,182,212,0.06);
    border: 1px solid rgba(6,182,212,0.18);
    border-radius: 12px;
    padding: 1rem 1rem;
    margin-top: 0.75rem;
}

.tip-card-title {
    font-family: 'Inter', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #06B6D4;
    margin-bottom: 0.45rem;
    display: flex;
    align-items: center;
    gap: 0.35rem;
}

.tip-card-body {
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    color: #94A3B8;
    line-height: 1.6;
}

/* ---- Inference time caption styling ---- */
.stChatMessage .stCaption, .stCaption {
    font-family: 'Inter', sans-serif !important;
}

/* ---- Footer ---- */
.footer {
    text-align: center;
    padding: 1.5rem 0 0.5rem 0;
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    color: #475569;
    letter-spacing: 0.02em;
}
</style>
""", unsafe_allow_html=True)


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


# =====================================================================
# SIDEBAR — Informasi kelompok & instruksi penggunaan
# =====================================================================
with st.sidebar:
    # ---- Branding header ----
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-logo">🎓</div>
        <div class="sidebar-brand">FAQ Akademik DTE</div>
    </div>
    <div class="sidebar-divider"></div>
    """, unsafe_allow_html=True)

    # ---- Konteks tugas ----
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">📋 Konteks Tugas</div>
        <div class="info-card-body">
            Tugas Pengganti UAS<br>
            <strong>Kecerdasan Buatan — 01</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- Kelompok ----
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">👥 Kelompok Rabu-18</div>
        <div class="info-card-body">
            <span class="member-name">Raka Arrayan Muttaqien</span><br>
            <span class="member-nim">2306161800</span><br><br>
            <span class="member-name">Daffa Hardhan</span><br>
            <span class="member-nim">2306161763</span><br><br>
            <span class="member-name">Wilman Saragih Sitio</span><br>
            <span class="member-nim">2306161776</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- Tips penggunaan ----
    st.markdown("""
    <div class="tip-card">
        <div class="tip-card-title">💡 Cara Menggunakan</div>
        <div class="tip-card-body">
            Ketik pertanyaan Anda seputar akademik DTE di kolom chat di bawah, lalu tekan <strong>Enter</strong>. 
            Chatbot akan mencari jawaban paling relevan dari basis data FAQ menggunakan <em>Sentence-BERT</em>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- Footer sidebar ----
    st.markdown("""
    <div class="sidebar-divider"></div>
    <div class="footer">
        Powered by <strong>Sentence-BERT</strong><br>
        Cosine Similarity Retrieval
    </div>
    """, unsafe_allow_html=True)


# =====================================================================
# MAIN AREA — Header hero + chat
# =====================================================================

# ---- Hero header ----
st.markdown("""
<div class="hero-container">
    <div class="hero-icon">🤖</div>
    <div class="hero-title">Chatbot FAQ Akademik<br>dengan Sentence-BERT</div>
    <div class="hero-subtitle">
        Asisten cerdas berbasis <em>Natural Language Processing</em> untuk menjawab pertanyaan 
        seputar regulasi dan informasi akademik Departemen Teknik Elektro.
    </div>
    <div class="badge-row">
        <span class="badge">🧠 Sentence-BERT</span>
        <span class="badge">📐 Cosine Similarity</span>
        <span class="badge">⚡ Real-time Retrieval</span>
    </div>
</div>
<div class="styled-divider"></div>
""", unsafe_allow_html=True)


# --- 2. Manajemen State (Session State) ---
# Menyimpan riwayat percakapan di memori browser pengguna agar chat tidak hilang.
if "messages" not in st.session_state:
    # Set pesan default dari bot di awal sesi
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Halo! Selamat datang di **FAQ Akademik DTE**.\n\nSaya adalah asisten cerdas yang siap membantu menjawab pertanyaan Anda seputar regulasi dan informasi akademik Departemen Teknik Elektro.\n\n💬 Silakan ketik pertanyaan Anda di kolom chat di bawah!"}
    ]


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
