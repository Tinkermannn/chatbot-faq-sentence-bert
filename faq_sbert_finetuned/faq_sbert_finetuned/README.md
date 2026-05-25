---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- generated_from_trainer
- dataset_size:335
- loss:CosineSimilarityLoss
base_model: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
widget:
- source_sentence: apakah bisa mengambil lebih dari satu sertifikat dari coursera
    untuk ditransferkreditkan menjadi beberapa mk pilihan
  sentences:
  - tolong jelaskan jam per minggu minggu kegiatan ppt 1 dilaksanakan
  - nilai sidang kerja praktik masuk hitungan indeks prestasi kumulatif gak
  - saya ingin tahu sidang seminar melibatkan dosen penguji selain pembimbing
- source_sentence: apa nilai minimal untuk pengakuan 1 sertifikat level associate
    di ppt 2
  sentences:
  - apakah di ui tersedia beasiswa
  - tolong jelaskan jika meraih juara 3 kompetisi tingkat nasional
  - kapan departemen menetapkan pembimbing selambat lambatnya
- source_sentence: berapa lama waktu yang dibutuhkan hingga surat jadi dapat diunduh
  sentences:
  - apakah benar sidang seminar melibatkan dosen penguji selain pembimbing
  - gimana cara mengetahui surat sudah siap diunduh
  - apa nomor whatsapp resmi dte ftui
- source_sentence: apakah mahasiswa bisa mengajukan keberatan atas penetapan pembimbing
    skripsi
  sentences:
  - laporan kerja praktik tidak dicap perusahaan gimana
  - apa saja kelengkapan berkas untuk pengakuan paper conference
  - kalau gak setuju sama dosbing skripsi yang ditetapkan
- source_sentence: bukti apa yang diperlukan untuk transfer kredit pembelajaran mandiri
  sentences:
  - mohon info cara mengetahui jadwal sidang kerja praktik
  - mohon info bukti diperlukan transfer kredit pembelajaran mandiri
  - saya ingin tahu proses pengajuan transfer kredit magang mandiri dilaksanakan
pipeline_tag: sentence-similarity
library_name: sentence-transformers
metrics:
- pearson_cosine
- spearman_cosine
model-index:
- name: SentenceTransformer based on sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
  results:
  - task:
      type: semantic-similarity
      name: Semantic Similarity
    dataset:
      name: dev similarity
      type: dev-similarity
    metrics:
    - type: pearson_cosine
      value: 0.9386053785802335
      name: Pearson Cosine
    - type: spearman_cosine
      value: 0.8391689071090089
      name: Spearman Cosine
---

# SentenceTransformer based on sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2). It maps sentences & paragraphs to a 384-dimensional dense vector space and can be used for retrieval.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) <!-- at revision e8f8c211226b894fcb81acc59f3b34ba3efd5f42 -->
- **Maximum Sequence Length:** 128 tokens
- **Output Dimensionality:** 384 dimensions
- **Similarity Function:** Cosine Similarity
- **Supported Modality:** Text
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'transformer_task': 'feature-extraction', 'modality_config': {'text': {'method': 'forward', 'method_output_name': 'last_hidden_state'}}, 'module_output_name': 'token_embeddings', 'architecture': 'BertModel'})
  (1): Pooling({'embedding_dimension': 384, 'pooling_mode': 'mean', 'include_prompt': True})
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```
Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    'bukti apa yang diperlukan untuk transfer kredit pembelajaran mandiri',
    'mohon info bukti diperlukan transfer kredit pembelajaran mandiri',
    'mohon info cara mengetahui jadwal sidang kerja praktik',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 384]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[1.0000, 0.9902, 0.0143],
#         [0.9902, 1.0000, 0.0124],
#         [0.0143, 0.0124, 1.0000]])
```
<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

## Evaluation

### Metrics

#### Semantic Similarity

* Dataset: `dev-similarity`
* Evaluated with [<code>EmbeddingSimilarityEvaluator</code>](https://sbert.net/docs/package_reference/sentence_transformer/evaluation.html#sentence_transformers.sentence_transformer.evaluation.EmbeddingSimilarityEvaluator)

| Metric              | Value      |
|:--------------------|:-----------|
| pearson_cosine      | 0.9386     |
| **spearman_cosine** | **0.8392** |

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Dataset

#### Unnamed Dataset

* Size: 335 training samples
* Columns: <code>sentence1</code>, <code>sentence2</code>, and <code>label</code>
* Approximate statistics based on the first 335 samples:
  |         | sentence1                                                                         | sentence2                                                                         | label                                                          |
  |:--------|:----------------------------------------------------------------------------------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------|
  | type    | string                                                                            | string                                                                            | float                                                          |
  | details | <ul><li>min: 6 tokens</li><li>mean: 14.24 tokens</li><li>max: 23 tokens</li></ul> | <ul><li>min: 6 tokens</li><li>mean: 13.44 tokens</li><li>max: 23 tokens</li></ul> | <ul><li>min: 0.0</li><li>mean: 0.48</li><li>max: 1.0</li></ul> |
* Samples:
  | sentence1                                                                                                | sentence2                                                               | label            |
  |:---------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------|:-----------------|
  | <code>apa saja program studi yang ada di dte</code>                                                      | <code>apa aja program studi yang ada di dte</code>                      | <code>1.0</code> |
  | <code>apa saja program studi yang ada di dte</code>                                                      | <code>bagaimana cara mendapatkan surat pengantar kerja praktik</code>   | <code>0.0</code> |
  | <code>berapa maksimal satuan kredit semester yang bisa diambil di semester saat mengambil skripsi</code> | <code>syarat satuan kredit semester untuk magang wajib berapa ya</code> | <code>0.0</code> |
* Loss: [<code>CosineSimilarityLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#cosinesimilarityloss) with these parameters:
  ```json
  {
      "loss_fct": "torch.nn.modules.loss.MSELoss",
      "cos_score_transformation": "torch.nn.modules.linear.Identity"
  }
  ```

### Evaluation Dataset

#### Unnamed Dataset

* Size: 83 evaluation samples
* Columns: <code>sentence1</code>, <code>sentence2</code>, and <code>label</code>
* Approximate statistics based on the first 83 samples:
  |         | sentence1                                                                         | sentence2                                                                        | label                                                          |
  |:--------|:----------------------------------------------------------------------------------|:---------------------------------------------------------------------------------|:---------------------------------------------------------------|
  | type    | string                                                                            | string                                                                           | float                                                          |
  | details | <ul><li>min: 6 tokens</li><li>mean: 14.66 tokens</li><li>max: 22 tokens</li></ul> | <ul><li>min: 7 tokens</li><li>mean: 13.2 tokens</li><li>max: 23 tokens</li></ul> | <ul><li>min: 0.0</li><li>mean: 0.43</li><li>max: 1.0</li></ul> |
* Samples:
  | sentence1                                                                                                               | sentence2                                                                                                                     | label            |
  |:------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------|:-----------------|
  | <code>kapan proses pengajuan transfer kredit magang mandiri harus dilaksanakan</code>                                   | <code>apakah bisa siswa jurusan ips mengambil prodi jurusan ipa</code>                                                        | <code>0.0</code> |
  | <code>apakah magang mandiri yang akan ditransferkreditkan menjadi magang wajib tetap harus mendaftar di d office</code> | <code>apakah benar magang mandiri yang akan ditransferkreditkan menjadi magang wajib tetap harus mendaftar di d office</code> | <code>1.0</code> |
  | <code>apakah di ui tersedia beasiswa</code>                                                                             | <code>apakah benar di ui tersedia beasiswa</code>                                                                             | <code>1.0</code> |
* Loss: [<code>CosineSimilarityLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#cosinesimilarityloss) with these parameters:
  ```json
  {
      "loss_fct": "torch.nn.modules.loss.MSELoss",
      "cos_score_transformation": "torch.nn.modules.linear.Identity"
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 4
- `per_device_eval_batch_size`: 4
- `num_train_epochs`: 2
- `warmup_steps`: 1

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `do_predict`: False
- `prediction_loss_only`: True
- `per_device_train_batch_size`: 4
- `per_device_eval_batch_size`: 4
- `gradient_accumulation_steps`: 1
- `eval_accumulation_steps`: None
- `torch_empty_cache_steps`: None
- `learning_rate`: 5e-05
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `max_grad_norm`: 1.0
- `num_train_epochs`: 2
- `max_steps`: -1
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: None
- `warmup_ratio`: None
- `warmup_steps`: 1
- `log_level`: passive
- `log_level_replica`: warning
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `enable_jit_checkpoint`: False
- `save_on_each_node`: False
- `save_only_model`: False
- `restore_callback_states_from_checkpoint`: False
- `use_cpu`: False
- `seed`: 42
- `data_seed`: None
- `bf16`: False
- `fp16`: False
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `local_rank`: -1
- `ddp_backend`: None
- `debug`: []
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_prefetch_factor`: None
- `disable_tqdm`: False
- `remove_unused_columns`: True
- `label_names`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `fsdp`: []
- `fsdp_config`: {'min_num_params': 0, 'xla': False, 'xla_fsdp_v2': False, 'xla_fsdp_grad_ckpt': False}
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `deepspeed`: None
- `label_smoothing_factor`: 0.0
- `optim`: adamw_torch_fused
- `optim_args`: None
- `group_by_length`: False
- `length_column_name`: length
- `project`: huggingface
- `trackio_space_id`: trackio
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `skip_memory_metrics`: True
- `push_to_hub`: False
- `resume_from_checkpoint`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_private_repo`: None
- `hub_always_push`: False
- `hub_revision`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `include_for_metrics`: []
- `eval_do_concat_batches`: True
- `auto_find_batch_size`: False
- `full_determinism`: False
- `ddp_timeout`: 1800
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `include_num_input_tokens_seen`: no
- `neftune_noise_alpha`: None
- `optim_target_modules`: None
- `batch_eval_metrics`: False
- `eval_on_start`: False
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `eval_use_gather_object`: False
- `average_tokens_across_devices`: True
- `use_cache`: False
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: proportional
- `router_mapping`: {}
- `learning_rate_mapping`: {}

</details>

### Training Logs
<details><summary>Click to expand</summary>

| Epoch  | Step | Training Loss | Validation Loss | dev-similarity_spearman_cosine |
|:------:|:----:|:-------------:|:---------------:|:------------------------------:|
| 0.0119 | 1    | 0.0497        | -               | -                              |
| 0.0238 | 2    | 0.0851        | -               | -                              |
| 0.0357 | 3    | 0.0587        | -               | -                              |
| 0.0476 | 4    | 0.0466        | -               | -                              |
| 0.0595 | 5    | 0.0288        | -               | -                              |
| 0.0714 | 6    | 0.0331        | -               | -                              |
| 0.0833 | 7    | 0.0571        | -               | -                              |
| 0.0952 | 8    | 0.0645        | -               | -                              |
| 0.1071 | 9    | 0.0548        | -               | -                              |
| 0.1190 | 10   | 0.0037        | -               | -                              |
| 0.1310 | 11   | 0.0627        | -               | -                              |
| 0.1429 | 12   | 0.0142        | -               | -                              |
| 0.1548 | 13   | 0.0142        | -               | -                              |
| 0.1667 | 14   | 0.0719        | -               | -                              |
| 0.1786 | 15   | 0.0545        | -               | -                              |
| 0.1905 | 16   | 0.0042        | -               | -                              |
| 0.2024 | 17   | 0.0150        | -               | -                              |
| 0.2143 | 18   | 0.0052        | -               | -                              |
| 0.2262 | 19   | 0.0182        | -               | -                              |
| 0.2381 | 20   | 0.0154        | -               | -                              |
| 0.25   | 21   | 0.1549        | -               | -                              |
| 0.2619 | 22   | 0.0124        | -               | -                              |
| 0.2738 | 23   | 0.0119        | -               | -                              |
| 0.2857 | 24   | 0.0708        | -               | -                              |
| 0.2976 | 25   | 0.0448        | -               | -                              |
| 0.3095 | 26   | 0.0103        | -               | -                              |
| 0.3214 | 27   | 0.0213        | -               | -                              |
| 0.3333 | 28   | 0.0076        | -               | -                              |
| 0.3452 | 29   | 0.0463        | -               | -                              |
| 0.3571 | 30   | 0.1168        | -               | -                              |
| 0.3690 | 31   | 0.0597        | -               | -                              |
| 0.3810 | 32   | 0.0965        | -               | -                              |
| 0.3929 | 33   | 0.0339        | -               | -                              |
| 0.4048 | 34   | 0.0425        | -               | -                              |
| 0.4167 | 35   | 0.0157        | -               | -                              |
| 0.4286 | 36   | 0.0048        | -               | -                              |
| 0.4405 | 37   | 0.0620        | -               | -                              |
| 0.4524 | 38   | 0.0593        | -               | -                              |
| 0.4643 | 39   | 0.0339        | -               | -                              |
| 0.4762 | 40   | 0.0138        | -               | -                              |
| 0.4881 | 41   | 0.0642        | -               | -                              |
| 0.5    | 42   | 0.0151        | 0.0315          | 0.8483                         |
| 0.5119 | 43   | 0.0791        | -               | -                              |
| 0.5238 | 44   | 0.0651        | -               | -                              |
| 0.5357 | 45   | 0.0270        | -               | -                              |
| 0.5476 | 46   | 0.0278        | -               | -                              |
| 0.5595 | 47   | 0.0563        | -               | -                              |
| 0.5714 | 48   | 0.1455        | -               | -                              |
| 0.5833 | 49   | 0.0377        | -               | -                              |
| 0.5952 | 50   | 0.0079        | -               | -                              |
| 0.6071 | 51   | 0.0226        | -               | -                              |
| 0.6190 | 52   | 0.0091        | -               | -                              |
| 0.6310 | 53   | 0.0109        | -               | -                              |
| 0.6429 | 54   | 0.1668        | -               | -                              |
| 0.6548 | 55   | 0.0323        | -               | -                              |
| 0.6667 | 56   | 0.0053        | -               | -                              |
| 0.6786 | 57   | 0.0179        | -               | -                              |
| 0.6905 | 58   | 0.0310        | -               | -                              |
| 0.7024 | 59   | 0.0107        | -               | -                              |
| 0.7143 | 60   | 0.0614        | -               | -                              |
| 0.7262 | 61   | 0.0136        | -               | -                              |
| 0.7381 | 62   | 0.0061        | -               | -                              |
| 0.75   | 63   | 0.0335        | -               | -                              |
| 0.7619 | 64   | 0.0178        | -               | -                              |
| 0.7738 | 65   | 0.0192        | -               | -                              |
| 0.7857 | 66   | 0.0018        | -               | -                              |
| 0.7976 | 67   | 0.1411        | -               | -                              |
| 0.8095 | 68   | 0.0179        | -               | -                              |
| 0.8214 | 69   | 0.0138        | -               | -                              |
| 0.8333 | 70   | 0.0055        | -               | -                              |
| 0.8452 | 71   | 0.0454        | -               | -                              |
| 0.8571 | 72   | 0.0612        | -               | -                              |
| 0.8690 | 73   | 0.0138        | -               | -                              |
| 0.8810 | 74   | 0.0290        | -               | -                              |
| 0.8929 | 75   | 0.0058        | -               | -                              |
| 0.9048 | 76   | 0.1207        | -               | -                              |
| 0.9167 | 77   | 0.0357        | -               | -                              |
| 0.9286 | 78   | 0.0055        | -               | -                              |
| 0.9405 | 79   | 0.0630        | -               | -                              |
| 0.9524 | 80   | 0.0077        | -               | -                              |
| 0.9643 | 81   | 0.0223        | -               | -                              |
| 0.9762 | 82   | 0.0529        | -               | -                              |
| 0.9881 | 83   | 0.0028        | -               | -                              |
| 1.0    | 84   | 0.1065        | 0.0280          | 0.8371                         |
| 1.0119 | 85   | 0.0489        | -               | -                              |
| 1.0238 | 86   | 0.0149        | -               | -                              |
| 1.0357 | 87   | 0.0430        | -               | -                              |
| 1.0476 | 88   | 0.0054        | -               | -                              |
| 1.0595 | 89   | 0.0226        | -               | -                              |
| 1.0714 | 90   | 0.0315        | -               | -                              |
| 1.0833 | 91   | 0.0086        | -               | -                              |
| 1.0952 | 92   | 0.0229        | -               | -                              |
| 1.1071 | 93   | 0.0354        | -               | -                              |
| 1.1190 | 94   | 0.0152        | -               | -                              |
| 1.1310 | 95   | 0.0056        | -               | -                              |
| 1.1429 | 96   | 0.0075        | -               | -                              |
| 1.1548 | 97   | 0.0053        | -               | -                              |
| 1.1667 | 98   | 0.0040        | -               | -                              |
| 1.1786 | 99   | 0.0155        | -               | -                              |
| 1.1905 | 100  | 0.0100        | -               | -                              |
| 1.2024 | 101  | 0.0022        | -               | -                              |
| 1.2143 | 102  | 0.0257        | -               | -                              |
| 1.2262 | 103  | 0.0080        | -               | -                              |
| 1.2381 | 104  | 0.0182        | -               | -                              |
| 1.25   | 105  | 0.0121        | -               | -                              |
| 1.2619 | 106  | 0.0242        | -               | -                              |
| 1.2738 | 107  | 0.0038        | -               | -                              |
| 1.2857 | 108  | 0.0176        | -               | -                              |
| 1.2976 | 109  | 0.0084        | -               | -                              |
| 1.3095 | 110  | 0.0138        | -               | -                              |
| 1.3214 | 111  | 0.0138        | -               | -                              |
| 1.3333 | 112  | 0.0106        | -               | -                              |
| 1.3452 | 113  | 0.0120        | -               | -                              |
| 1.3571 | 114  | 0.0321        | -               | -                              |
| 1.3690 | 115  | 0.0253        | -               | -                              |
| 1.3810 | 116  | 0.0167        | -               | -                              |
| 1.3929 | 117  | 0.0043        | -               | -                              |
| 1.4048 | 118  | 0.0252        | -               | -                              |
| 1.4167 | 119  | 0.0038        | -               | -                              |
| 1.4286 | 120  | 0.0100        | -               | -                              |
| 1.4405 | 121  | 0.0046        | -               | -                              |
| 1.4524 | 122  | 0.0043        | -               | -                              |
| 1.4643 | 123  | 0.0036        | -               | -                              |
| 1.4762 | 124  | 0.1187        | -               | -                              |
| 1.4881 | 125  | 0.0012        | -               | -                              |
| 1.5    | 126  | 0.0112        | 0.0299          | 0.8371                         |
| 1.5119 | 127  | 0.0089        | -               | -                              |
| 1.5238 | 128  | 0.0093        | -               | -                              |
| 1.5357 | 129  | 0.0230        | -               | -                              |
| 1.5476 | 130  | 0.0052        | -               | -                              |
| 1.5595 | 131  | 0.0123        | -               | -                              |
| 1.5714 | 132  | 0.0043        | -               | -                              |
| 1.5833 | 133  | 0.0229        | -               | -                              |
| 1.5952 | 134  | 0.0195        | -               | -                              |
| 1.6071 | 135  | 0.0009        | -               | -                              |
| 1.6190 | 136  | 0.0044        | -               | -                              |
| 1.6310 | 137  | 0.0042        | -               | -                              |
| 1.6429 | 138  | 0.0127        | -               | -                              |
| 1.6548 | 139  | 0.0269        | -               | -                              |
| 1.6667 | 140  | 0.0178        | -               | -                              |
| 1.6786 | 141  | 0.0376        | -               | -                              |
| 1.6905 | 142  | 0.0031        | -               | -                              |
| 1.7024 | 143  | 0.0310        | -               | -                              |
| 1.7143 | 144  | 0.0026        | -               | -                              |
| 1.7262 | 145  | 0.0221        | -               | -                              |
| 1.7381 | 146  | 0.0034        | -               | -                              |
| 1.75   | 147  | 0.0085        | -               | -                              |
| 1.7619 | 148  | 0.0082        | -               | -                              |
| 1.7738 | 149  | 0.0345        | -               | -                              |
| 1.7857 | 150  | 0.0055        | -               | -                              |
| 1.7976 | 151  | 0.0030        | -               | -                              |
| 1.8095 | 152  | 0.0275        | -               | -                              |
| 1.8214 | 153  | 0.0181        | -               | -                              |
| 1.8333 | 154  | 0.0263        | -               | -                              |
| 1.8452 | 155  | 0.0207        | -               | -                              |
| 1.8571 | 156  | 0.0306        | -               | -                              |
| 1.8690 | 157  | 0.0048        | -               | -                              |
| 1.8810 | 158  | 0.0156        | -               | -                              |
| 1.8929 | 159  | 0.0249        | -               | -                              |
| 1.9048 | 160  | 0.0067        | -               | -                              |
| 1.9167 | 161  | 0.0201        | -               | -                              |
| 1.9286 | 162  | 0.0334        | -               | -                              |
| 1.9405 | 163  | 0.0032        | -               | -                              |
| 1.9524 | 164  | 0.0110        | -               | -                              |
| 1.9643 | 165  | 0.0133        | -               | -                              |
| 1.9762 | 166  | 0.0081        | -               | -                              |
| 1.9881 | 167  | 0.0151        | -               | -                              |
| 2.0    | 168  | 0.0208        | 0.0301          | 0.8392                         |

</details>

### Training Time
- **Training**: 4.5 minutes

### Framework Versions
- Python: 3.12.13
- Sentence Transformers: 5.4.1
- Transformers: 5.0.0
- PyTorch: 2.10.0+cpu
- Accelerate: 1.13.0
- Datasets: 4.0.0
- Tokenizers: 0.22.2

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->