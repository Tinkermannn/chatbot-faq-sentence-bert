import json
import pickle
import re

import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util



SINGKATAN = {
    'kp': 'kerja praktik',
    'ta': 'tugas akhir',
    'pkl': 'praktik kerja lapangan',
    'ipk': 'indeks prestasi kumulatif',
    'nim': 'nomor induk mahasiswa',
    'nip': 'nomor induk pegawai',
    'sks': 'satuan kredit semester',
    'krs': 'kartu rencana studi',
    'khs': 'kartu hasil studi',
    'uts': 'ujian tengah semester',
    'uas': 'ujian akhir semester',
}


def normalize_text(text):
    """Gunakan normalisasi yang konsisten dengan notebook eksperimen."""
    text = str(text).strip().lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    words = text.split()
    words = [SINGKATAN.get(word, word) for word in words]
    return ' '.join(words)


class FAQEngine:
    def __init__(self, model_name_or_path='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', threshold=0.45):
        """
        Inisialisasi FAQ Engine dengan arsitektur Bi-Encoder (Sentence-BERT).
        :param model_name_or_path: Nama model Hugging Face atau path ke folder model lokal (misal: 'faq_sbert_finetuned')
        :param threshold: Batas minimal Cosine Similarity (0.0 - 1.0) untuk menolak pertanyaan Out-of-Domain (OOD).
        """
        self.threshold = threshold

        # Load model Sentence-BERT ke memori. Proses ini cukup berat,
        # sehingga sangat penting untuk di-cache pada sisi UI (Streamlit).
        self.model = SentenceTransformer(model_name_or_path)

        # Properti untuk menampung data corpus FAQ.
        # questions_clean dipakai bila artefak JSON juga menyimpan versi yang sudah dinormalisasi.
        self.questions = []
        self.questions_clean = []
        self.answers = []
        self.embeddings = None

    def load_data(self, json_path='faq_data.json', npy_path='faq_embeddings.npy', pkl_path='faq_data.pkl'):
        """
        Memuat data FAQ dan matriks embeddings.

        Jika pkl_path diberikan, data dimuat langsung dari file pickle hasil notebook.
        Jika tidak, data dimuat dari pasangan file JSON + Numpy.
        """
        if pkl_path:
            with open(pkl_path, 'rb') as f:
                data = pickle.load(f)

            self.questions = data.get('questions', [])
            self.questions_clean = data.get('questions_clean', [])
            self.answers = data.get('answers', [])

            if 'threshold' in data:
                self.threshold = float(data['threshold'])

            if not self.questions_clean:
                self.questions_clean = [normalize_text(question) for question in self.questions]

            self.embeddings = torch.tensor(data['embeddings'])
            return

        # 1. Load teks pertanyaan dan jawaban
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.questions = data.get('questions', [])
            self.questions_clean = data.get('questions_clean', [])
            self.answers = data.get('answers', [])

            # Jika artefak menyimpan threshold terbaik dari notebook, gunakan nilai itu.
            if 'threshold' in data:
                self.threshold = float(data['threshold'])

        # Fallback untuk artefak lama yang belum menyimpan questions_clean.
        if not self.questions_clean:
            self.questions_clean = [normalize_text(question) for question in self.questions]

        # 2. Load matriks vektor (embeddings) yang sudah di-precompute (Numpy array)
        embeddings_np = np.load(npy_path)

        # Konversi array Numpy ke dalam bentuk Tensor PyTorch
        # agar komputasi Cosine Similarity berjalan optimal.
        self.embeddings = torch.tensor(embeddings_np)

    def retrieve_answer_with_matches(self, query, top_k=3):
        """
        Mencari jawaban terbaik beserta kandidat pertanyaan terdekat.
        """
        if self.embeddings is None:
            return {
                "answer": "Sistem belum siap. Data embeddings tidak ditemukan.",
                "score": 0.0,
                "matches": [],
                "is_fallback": True,
            }

        # Query user harus dibersihkan dengan aturan yang sama seperti di notebook.
        # Tanpa ini, istilah seperti "KP" vs "kerja praktik" akan mismatch.
        normalized_query = normalize_text(query)

        # Encode kalimat user menjadi representasi vektor secara dinamis.
        query_embedding = self.model.encode(
            normalized_query,
            convert_to_tensor=True,
            normalize_embeddings=True
        )

        # Hitung skor kesamaan semantik antara query dan seluruh FAQ.
        scores = util.cos_sim(query_embedding, self.embeddings)[0]

        # Ambil kandidat teratas. Walau jawaban akhir tetap Top-1, top_k dipertahankan
        # agar mudah diperluas untuk debugging atau menampilkan kandidat alternatif.
        top_results = scores.topk(k=min(top_k, len(self.questions)))

        best_score = float(top_results.values[0])
        best_idx = int(top_results.indices[0])
        best_question = self.questions[best_idx]
        matches = [
            {
                "question": self.questions[int(idx)],
                "score": float(score),
            }
            for score, idx in zip(top_results.values, top_results.indices)
        ]

        # --- DEBUGGING SNIPPET ---
        print("\n" + "=" * 50)
        print(f"[DEBUG] Input User   : '{query}'")
        print(f"[DEBUG] Normalized   : '{normalized_query}'")
        print(f"[DEBUG] Top-1 Match  : '{best_question}'")
        print(f"[DEBUG] Similarity   : {best_score:.4f} (Threshold: {self.threshold})")
        if best_score < self.threshold:
            print("[DEBUG] STATUS       : FALLBACK (Skor di bawah threshold)")
        else:
            print("[DEBUG] STATUS       : LOLOS (Skor di atas threshold)")
        print("=" * 50 + "\n")
        # -------------------------

        # Jika skor kemiripan berada di bawah threshold, tolak untuk menjawab.
        if best_score < self.threshold:
            return {
                "answer": "Maaf, saya tidak menemukan informasi yang relevan terkait pertanyaan Anda atau pertanyaan tersebut berada di luar topik akademik kami.",
                "score": best_score,
                "matches": matches,
                "is_fallback": True,
            }

        # Jika lolos validasi threshold, kembalikan jawaban terbaik.
        return {
            "answer": self.answers[best_idx],
            "score": best_score,
            "matches": matches,
            "is_fallback": False,
        }

    def retrieve_answer(self, query, top_k=3):
        """
        Mencari jawaban terbaik berdasarkan pertanyaan user menggunakan Cosine Similarity.
        """
        return self.retrieve_answer_with_matches(query, top_k=top_k)["answer"]