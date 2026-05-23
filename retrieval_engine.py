import json
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util

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
        
        # Properti untuk menampung data corpus FAQ
        self.questions = []
        self.answers = []
        self.embeddings = None

    def load_data(self, json_path='faq_data.json', npy_path='faq_embeddings.npy'):
        """
        Memuat data teks FAQ dari file JSON dan matriks embeddings dari file Numpy.
        Metode ini menghindari celah keamanan dari penggunaan file .pkl (pickle).
        """
        # 1. Load teks pertanyaan dan jawaban
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.questions = data.get('questions', [])
            self.answers = data.get('answers', [])
            
        # 2. Load matriks vektor (embeddings) yang sudah di-precompute (Numpy array)
        embeddings_np = np.load(npy_path)
        
        # Konversi array Numpy ke dalam bentuk Tensor PyTorch
        # Agar komputasi jarak vektor (Cosine Similarity) berjalan secara optimal
        self.embeddings = torch.tensor(embeddings_np)
        
    def retrieve_answer(self, query, top_k=3):
        """
        Mencari jawaban terbaik berdasarkan pertanyaan user menggunakan perhitungan Cosine Similarity.
        """
        if self.embeddings is None:
            return "Sistem belum siap. Data embeddings tidak ditemukan."
            
        # Encode kalimat user menjadi representasi vektor secara dinamis
        query_embedding = self.model.encode(query, convert_to_tensor=True, normalize_embeddings=True)
        
        # Hitung skor kesamaan jarak semantik (kosinus) antara vektor query dengan vektor data FAQ
        scores = util.cos_sim(query_embedding, self.embeddings)[0]
        
        # Ambil skor tertinggi beserta posisinya (indeks)
        top_results = scores.topk(k=1) # Ambil yang paling tinggi (Top-1)
        
        best_score = float(top_results.values[0])
        best_idx = int(top_results.indices[0])
        best_question = self.questions[best_idx]
        
        # --- DEBUGGING SNIPPET ---
        print("\n" + "="*50)
        print(f"[DEBUG] Input User   : '{query}'")
        print(f"[DEBUG] Top-1 Match  : '{best_question}'")
        print(f"[DEBUG] Similarity   : {best_score:.4f} (Threshold: {self.threshold})")
        if best_score < self.threshold:
            print("[DEBUG] STATUS       : ❌ FALLBACK (Skor di bawah threshold)")
        else:
            print("[DEBUG] STATUS       : ✅ LOLOS (Skor di atas threshold)")
        print("="*50 + "\n")
        # -------------------------
        
        # --- Deteksi Out-of-Domain (OOD) menggunakan Threshold Fallback ---
        # Jika skor kemiripan berada di bawah batas minimum (0.45), tolak untuk menjawab.
        if best_score < self.threshold:
            return "Maaf, saya tidak menemukan informasi yang relevan terkait pertanyaan Anda atau pertanyaan tersebut berada di luar topik akademik kami."
            
        # Jika lolos validasi threshold, kembalikan jawaban terbaik
        return self.answers[best_idx]
