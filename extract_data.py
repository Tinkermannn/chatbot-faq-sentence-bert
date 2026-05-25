import pickle
import json
import numpy as np
import os

def extract_pickle_to_safe_formats(pkl_path='faq_data.pkl'):
    """
    Mengekstrak file faq_data.pkl buatan Colab menjadi format standar industri (JSON & Numpy).
    Ini menghindari celah keamanan (RCE) saat memuat file pickle langsung di production.
    """
    if not os.path.exists(pkl_path):
        print(f"File {pkl_path} tidak ditemukan. Pastikan file ada di direktori kerja.")
        return

    print("Membaca data dari pickle...")
    with open(pkl_path, 'rb') as f:
        data = pickle.load(f)

    # 1. Ekstrak data teks menjadi JSON
    json_data = {
        "questions": data.get("questions", []),
        "answers": data.get("answers", []),
        "questions_clean": data.get("questions_clean", []),
        "faq_ids": data.get("faq_ids", []),
        "threshold": data.get("threshold", 0.45)
    }

    with open('faq_data.json', 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    print("Berhasil mengekstrak data teks ke 'faq_data.json'")

    # 2. Ekstrak matriks embeddings menjadi Numpy array (.npy)
    embeddings = data.get("embeddings")
    if embeddings is not None:
        np.save('faq_embeddings.npy', embeddings)
        print(f"Berhasil mengekstrak matriks embeddings dengan dimensi {embeddings.shape} ke 'faq_embeddings.npy'")
    else:
        print("Peringatan: Tidak ditemukan matriks embeddings di dalam file pickle.")

if __name__ == "__main__":
    extract_pickle_to_safe_formats(pkl_path='data/output/faq_data.pkl')
