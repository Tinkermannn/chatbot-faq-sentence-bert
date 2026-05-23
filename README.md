# 🎓 Chatbot FAQ Akademik (Sentence-BERT)

<!-- Badges -->
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C.svg?style=flat&logo=pytorch)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=flat&logo=streamlit)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-F9AB00.svg?style=flat&logo=huggingface)

> **Tugas Pengganti UAS Kecerdasan Buatan - 01**  
> Teknik Komputer, Universitas Indonesia  
> **Kelompok:** Rabu-18

### 👨‍💻 Anggota Tim:
| Nama | NPM |
| :--- | :--- |
| **RAKA ARRAYAN MUTTAQIEN** | 2306161800 |
| **DAFFA HARDHAN** | 2306161763 |
| **WILMAN SARAGIH SITIO** | 2306161776 |

---

## 📖 Latar Belakang Proyek
Pencarian informasi akademik kampus seringkali terkendala oleh sistem yang hanya mengandalkan kecocokan kata kunci (*keyword matching*). Jika mahasiswa menggunakan singkatan, sinonim, bahasa gaul, atau terdapat kesalahan pengetikan (*typo*), sistem pencarian tradisional sering gagal memberikan jawaban. 

Proyek ini dibangun sebagai sistem pencarian informasi akademik pintar (*Semantic Search*) berbasis *Natural Language Processing* (NLP). Menggunakan arsitektur **Sentence-BERT (Bi-Encoder)**, chatbot ini mampu memahami *makna semantik* dari kalimat pengguna dan mencocokkannya dengan *Knowledge Base* FAQ akademik secara presisi.

---

## 🏗️ Arsitektur & Alur Kerja
Sistem ini dirancang menggunakan alur pengembangan *Machine Learning* yang terstruktur (*End-to-End*):

1. **Data Ingestion (`data/raw`):** Dataset mentah FAQ dikumpulkan dalam format CSV, terdiri dari 90 pasang pertanyaan-jawaban inti, serta data pelengkap (*similarity pairs*) untuk melatih kemampuan model memahami parafrase.
2. **Fine-Tuning SBERT (`.ipynb` di Google Colab):** Model bahasa dasar (`paraphrase-multilingual-MiniLM-L12-v2`) di-*fine-tune* menggunakan *CosineSimilarityLoss*. Pertanyaan FAQ kemudian diubah menjadi vektor (matriks *embeddings* 384-Dimensi) dan diekspor ke dalam kontainer `.pkl`.
3. **ETL Process (`extract_data.py`):** Demi mencapai standar keamanan produksi (menghindari kerentanan peretasan dari file *pickle*), file `.pkl` diekstrak dan ditransformasi menjadi format industri yang statis: `faq_data.json` (untuk metadata teks) dan `faq_embeddings.npy` (untuk pemrosesan tensor Numpy).
4. **Inference & UI (`app.py` & `retrieval_engine.py`):** Aplikasi Streamlit merender antarmuka obrolan (*chatbot UI*). Sistem menghitung jarak kosinus (*Cosine Similarity*) antara *query* pengguna dengan matriks FAQ secara instan (dioptimasi menggunakan memori *caching*).

---

## 📂 Struktur Direktori

```text
📦 chatbot-faq-sentence-bert
 ┣ 📂 data
 ┃ ┗ 📂 raw                      # Dataset mentah CSV (faq, similarity_pairs, OOD queries)
 ┣ 📂 faq_sbert_finetuned        # Folder model Sentence-BERT hasil fine-tuning
 ┣ 📜 app.py                     # Skrip utama antarmuka (Frontend) Streamlit UI
 ┣ 📜 retrieval_engine.py        # Core backend untuk loading SBERT & perhitungan kosinus
 ┣ 📜 extract_data.py            # Skrip ETL migrasi data dari format .pkl ke .json dan .npy
 ┣ 📜 chatbot_faq_sbert_colab.ipynb # Notebook laboratorium untuk preprocessing dan training
 ┣ 📜 faq_data.json              # Knowledge Base produksi (kumpulan FAQ)
 ┣ 📜 faq_embeddings.npy         # Matriks vektor Numpy untuk kalkulasi jarak Euclidean/Cosine
 ┣ 📜 .gitignore                 # Konfigurasi file yang tidak diunggah ke repositori Git
 ┗ 📜 README.md                  # Dokumentasi proyek (file ini)
```

### 🔍 Penjelasan Detail File:
*   **`app.py`**: Mengontrol logika tampilan *browser*, animasi *loading* asisten, dan manajemen memori sesi riwayat obrolan (*st.session_state*). Skrip ini memuat *decorator* `@st.cache_resource` agar model raksasa tidak *Out-of-Memory* (OOM).
*   **`retrieval_engine.py`**: Bertindak sebagai *Back-End Engine*. Kelas `FAQEngine` menangani logika komputasi tensor *Top-1 Match*. Pada file ini pula diletakkan algoritma *Fallback Detection* (OOD). Tersedia *debugging snippet* agar nilai kecocokan model bisa diinspeksi secara *real-time* di terminal VS Code.
*   **`extract_data.py`**: Skrip utilitas (*utility script*) yang mengubah hasil *dump* dari Google Colab menjadi aset siap *deploy*.
*   **`faq_sbert_finetuned/`**: Jantung dari kecerdasan bot ini. Berisi arsitektur Transformer dan *weights* yang telah berhasil memahami terminologi lokal kampus (seperti IRS, D'Office, SKS, dan KP) jauh melampaui kemampuan model pra-latih bawaannya.

---

## ✨ Fitur Utama
1. **Semantic Search Superior:** Tidak bergantung pada kecocokan teks eksak. Chatbot ini kebal terhadap *typo* ekstrem dan sangat toleran terhadap variasi kalimat (parafrase).
2. **Out-of-Domain (OOD) Detection:** Dibekali perlindungan *Anti-Halusinasi*. Menggunakan mekanisme *Thresholding* mutlak (misal: `< 0.45`). Jika pengguna iseng bertanya tentang resep makanan atau politik, sistem akan dengan cerdas menyadari bahwa topik tersebut bukan kewenangannya, lalu melakukan *Fallback* dengan merespon kalimat standar: *"Maaf, informasi di luar topik akademik"*.
3. **Session Memory UI:** Antarmuka responsif yang menyimpan riwayat obrolan secara persisten, tidak mereset layar setiap kali pengguna mengirimkan pesan baru, meniru pengalaman aplikasi perpesanan industri seperti WhatsApp.

---

## 🚀 Panduan Instalasi & Eksekusi (Lokal)

Ikuti instruksi bertahap ini untuk menjalankan repositori secara lokal.

**1. Clone Repository**
```bash
git clone https://github.com/username-anda/chatbot-faq-sentence-bert.git
cd chatbot-faq-sentence-bert
```

**2. Instalasi Requirements**
Pastikan *environment* Python Anda memiliki versi `3.8+`.
```bash
pip install streamlit sentence-transformers torch numpy pandas
```

**3. Ekstraksi Format Data Produksi (Sekali Jalan)**
Ekstrak arsip pengembangan biner (`faq_data.pkl`) menjadi arsitektur file JSON & Numpy yang sangat stabil.
```bash
python extract_data.py
```

**4. Jalankan Aplikasi AI Streamlit**
Nyalakan *local server* UI menggunakan perintah dasar Streamlit:
```bash
streamlit run app.py
```
*Aplikasi akan otomatis terbuka pada jendela browser Anda di alamat `http://localhost:8501`.*

---

## 🧪 Skenario Pengujian (Test Cases)

Di bawah ini adalah 3 eksperimen fungsionalitas yang wajib didemonstrasikan untuk membuktikan kapabilitas *Sentence-BERT* dan mekanisme perlindungan *Threshold* aplikasi ini.

| Kategori Pengujian | Contoh Input (*User Query*) | Ekspektasi Respons Sistem |
| :--- | :--- | :--- |
| **✅ Ideal Case** <br> *(In-Domain)* | `"Apa saja berkas yang harus diunggah saat mendaftar sidang KP di D'Office?"` | Membalas dengan informasi **3 syarat mutlak** sidang KP (Laporan + TTD industri, Log aktivitas, URL Rekaman). |
| **🔥 Robustness** <br> *(Typo & Bahasa Gaul)* | `"syrt dftr magang mandir di perushn yg blom krjasama sm dte gmna crnya??"` | Mampu menerjemahkan frasa kacau tersebut dan menjawab dengan tepat tata cara **Konsultasi dengan Tim Transfer Kredit (Tim TK)**. |
| **⛔ Out-of-Domain** <br> *(Deteksi OOD/Fallback)* | `"Gimana cara masak nasi goreng seafood?"` atau `"Siapa nama presiden saat ini?"` | Sistem memicu fitur keamanannya karena skor kesamaan (*Cosine Similarity*) anjlok jauh di bawah `0.45` dan merespon: *"Maaf, informasi tidak relevan..."* |

---