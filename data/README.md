# Folder Data

Folder ini dipakai agar file pendukung project tetap rapi, walaupun eksekusi utama tetap dilakukan dari satu notebook Colab.

## Isi Folder

- `raw/faq.csv`
  Salinan dataset FAQ utama.

- `raw/similarity_pairs.csv`
  Pasangan kalimat positif dan negatif untuk fine-tuning semantic similarity.

- `raw/faq_eval_queries.csv`
  Query evaluasi untuk mengukur apakah chatbot memilih FAQ yang benar.

- `raw/faq_ood_queries.csv`
  Query out-of-domain untuk demonstrasi threshold tuning dan fallback response.

## Catatan

Kamu tetap bisa menjalankan project hanya dari:

- `chatbot_faq_sbert_colab.ipynb`
- `faq.csv`

Folder ini disediakan agar dataset pendukung tidak bercampur di root folder.
