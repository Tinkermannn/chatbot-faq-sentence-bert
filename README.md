# Chatbot FAQ Akademik DTE Berbasis Sentence-BERT

## Ringkasan Proyek
Proyek ini merupakan implementasi sistem *question answering* berbasis *retrieval* untuk domain FAQ akademik Departemen Teknik Elektro (DTE). Sistem memanfaatkan model **Sentence-BERT** untuk merepresentasikan pertanyaan dalam ruang vektor, kemudian memilih jawaban paling relevan menggunakan **Cosine Similarity**.

Aplikasi disajikan dalam antarmuka web interaktif menggunakan **Streamlit**, sehingga pengguna dapat bertanya secara natural melalui chat.

## Tujuan
1. Membangun chatbot akademik yang mampu menjawab pertanyaan FAQ secara semantik (bukan hanya pencocokan kata kunci).
2. Mengurangi jawaban keliru melalui mekanisme *threshold* untuk mendeteksi pertanyaan di luar cakupan (*out-of-domain*).
3. Menyediakan prototipe yang dapat diuji langsung untuk kebutuhan tugas/pembelajaran Kecerdasan Buatan.

## Ruang Lingkup
- Domain terbatas pada informasi akademik DTE yang tersedia pada dataset FAQ.
- Pendekatan yang digunakan adalah **retrieval-based QA** (tanpa generasi jawaban baru).
- Jawaban diambil dari basis jawaban yang sudah tersedia pada data FAQ.

## Arsitektur Sistem
1. **Pra-pemrosesan teks**
- Normalisasi huruf kecil, penghapusan tanda baca, dan perapian spasi.
- Ekspansi singkatan akademik (contoh: `kp -> kerja praktik`, `ta -> tugas akhir`).

2. **Representasi semantik**
- Pertanyaan pengguna di-*encode* menggunakan model Sentence-BERT hasil *fine-tuning*.
- Embedding FAQ korpus disimpan terlebih dahulu (*precomputed embeddings*).

3. **Pencarian jawaban**
- Hitung Cosine Similarity antara embedding query dan seluruh embedding FAQ.
- Ambil kandidat teratas (*top-k*), lalu pilih *top-1* sebagai jawaban utama.

4. **Validasi domain**
- Jika skor kemiripan < *threshold* (default `0.45`), sistem memberikan respons fallback.

## Struktur Proyek
```text
finpro-ai/
|-- app.py
|-- retrieval_engine.py
|-- extract_data.py
|-- requirements.txt
|-- chatbot_faq_sbert_ai_rabu-18.ipynb
|-- data/
|   |-- README.md
|   |-- raw/
|   |   |-- faq.csv
|   |   |-- similarity_pairs.csv
|   |   |-- faq_eval_queries.csv
|   |   `-- faq_ood_queries.csv
|   `-- output/
|       `-- faq_data.pkl
`-- faq_sbert_finetuned/
    `-- faq_sbert_finetuned/
        |-- config*.json
        |-- tokenizer*.json
        |-- modules.json
        |-- model.safetensors
        `-- 1_Pooling/config.json
```

## Komponen Utama
- `app.py`: antarmuka chatbot berbasis Streamlit.
- `retrieval_engine.py`: inti logika retrieval, normalisasi teks, dan seleksi jawaban.
- `extract_data.py`: utilitas konversi artefak `pickle` menjadi format lebih aman (`JSON` dan `NPY`).
- `data/output/faq_data.pkl`: artefak yang memuat pertanyaan, jawaban, embedding, dan nilai threshold.
- `faq_sbert_finetuned/...`: model Sentence-BERT hasil *fine-tuning* yang dipakai saat inferensi.

## Dependensi
Daftar pustaka utama (sesuai `requirements.txt`):
- `streamlit`
- `sentence-transformers`
- `torch`
- `numpy`

## Instalasi dan Menjalankan Aplikasi
1. (Opsional) Buat virtual environment.
2. Instal dependensi:
```bash
pip install -r requirements.txt
```
3. Jalankan aplikasi:
```bash
streamlit run app.py
```
4. Buka URL lokal yang ditampilkan Streamlit di browser.

## Alur Penggunaan
1. Pengguna mengetik pertanyaan pada kolom chat.
2. Sistem menormalisasi pertanyaan dan menghitung embedding query.
3. Sistem mencari FAQ terdekat berdasarkan Cosine Similarity.
4. Sistem menampilkan:
- jawaban utama,
- kandidat pertanyaan terkait (*top-3*),
- waktu inferensi.

## Catatan Evaluasi Model
Berdasarkan *model card* pada folder model:
- Basis model: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- Dimensi embedding: `384`
- Metrik semantic similarity (dev):
- Pearson cosine: `0.9386`
- Spearman cosine: `0.8392`

## Keterbatasan
- Sistem tidak menghasilkan jawaban baru; kualitas jawaban bergantung pada kelengkapan FAQ.
- Domain sempit (akademik DTE), sehingga pertanyaan di luar domain akan diarahkan ke fallback.
- Nilai threshold saat ini masih statis dan dapat ditingkatkan melalui eksperimen lanjutan.

## Pengembangan Lanjutan
1. Menambah variasi data FAQ dan query evaluasi untuk meningkatkan cakupan.
2. Kalibrasi threshold adaptif berbasis validasi terpisah.
3. Menyimpan log anonim interaksi untuk analisis kesalahan dan perbaikan model.
4. Menambahkan pipeline evaluasi otomatis (akurasi top-1, top-k, dan OOD detection).

## Identitas Tim
Kelompok Rabu-18
- Raka Arrayan Muttaqien (2306161800)
- Daffa Hardhan (2306161763)
- Wilman Saragih Sitio (2306161776)

## Referensi Singkat
- Reimers, N., & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*.
- Dokumentasi Sentence-Transformers: https://www.sbert.net/
