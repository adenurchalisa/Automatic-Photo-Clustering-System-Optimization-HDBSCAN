# Automatic Photo Clustering System Optimization — HDBSCAN

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/adenurchalisa/Automatic-Photo-Clustering-System-Optimization-HDBSCAN/blob/main/notebooks/)

## Gambaran Umum

Repository ini berisi pipeline eksperimen lengkap untuk skripsi:

> **"Sistem Pengelompokan Foto Otomatis dan Penanganan Kondisi Few-Shot Menggunakan Algoritma HDBSCAN dan Augmentasi Data Generatif"**
>
> Ade Nurchalisa — UIN Alauddin Makassar

---

## Pertanyaan Penelitian

1. **RQ1**: Bagaimana merancang sistem pengelompokan otomatis yang efektif untuk foto dokumentasi yang tidak terstruktur?

2. **RQ2**: Bagaimana mengatasi kategori foto dengan jumlah sampel sangat sedikit (*few-shot*) yang menyebabkan algoritma clustering kesulitan membentuk cluster kecil?

---

## Metodologi

### Pipeline Utama

```
Dataset Foto
    │
    ├── Feature Extraction
    │       ├── InsightFace buffalo_l  → 512-dim face embeddings (NB1–NB8)
    │       └── CLIP ViT-L/14         → 768-dim photo embeddings (NB15)
    │
    ├── Clustering Optimization
    │       ├── Hyperparameter tuning HDBSCAN (NB1–NB5)
    │       ├── Distance metric comparison incl. QJSD (NB6)
    │       ├── Re-tuning dengan Correlation metric (NB8)
    │       ├── UMAP dimensionality reduction (NB9)
    │       ├── Angular + Soft Clustering (NB10)
    │       └── CLIP + UMAP + HDBSCAN (NB16)
    │
    └── Augmentation (Few-Shot Handling)
            ├── CGA — Cluster-Guided Gaussian Augmentation (NB12)
            └── NT-CGA — Noise-Targeted CGA (NB13)
```

---

## Struktur Notebook

| Notebook | Judul | Keterangan |
|---|---|---|
| NB1 | Eksperimen HDBSCAN Hyperparameter (1) | Eksplorasi awal `min_cluster_size` & `min_samples` |
| NB2 | Eksperimen HDBSCAN Hyperparameter (2) | Lanjutan grid search hyperparameter |
| NB3 | EDA & Baseline Clustering | Analisis data, visualisasi distribusi, baseline |
| NB4 | Fokus Hyperparameter | Penyempitan rentang hyperparameter |
| NB5 | Granular Hyperparameter | Fine-grained tuning parameter terpilih |
| NB6 | Distance Metric Comparison | Perbandingan metrik jarak termasuk **QJSD** (Quantum Jensen-Shannon Divergence, GPU-accelerated) vs Euclidean |
| NB8 | Re-Tuning Correlation | Re-tuning dengan metrik Correlation terbaik |
| NB9 | UMAP + HDBSCAN Pipeline | Reduksi dimensi UMAP sebelum HDBSCAN |
| NB10 | Angular Distance + Soft Clustering | Soft clustering dengan angular distance |
| NB11 | Analisis Komposisi Noise | Analisis mendalam penyebab dan komposisi noise |
| NB12 | CGA Augmentation | Cluster-Guided Gaussian Augmentation untuk few-shot |
| NB13 | NT-CGA Augmentation | Noise-Targeted CGA untuk cluster kecil & noise |
| NB14 | Final Evaluation | Evaluasi akhir dan perbandingan semua metode |
| NB15 | CLIP Feature Extraction | Ekstraksi embedding foto dengan CLIP ViT-L/14 |
| NB16 | CLIP + HDBSCAN Clustering | Clustering CLIP embeddings, grid search, UMAP+HDBSCAN |

---

## Ringkasan Hasil

### NB6 — Distance Metric Comparison (mcs=20, ms=50)

| Metrik | Clusters | Noise | Silhouette | Keterangan |
|---|---|---|---|---|
| **Euclidean** | **44** | **69.3%** | **0.3119** | **Terbaik — dijadikan baseline lanjut** |
| QJSD (GPU/CuPy) | 64 | 36.3% | 0.1308 | Virosztek (2021); noise lebih rendah tapi silhouette lebih rendah |

> **Catatan**: DBI tidak dihitung untuk QJSD karena sklearn hardcode Euclidean sehingga hasilnya tidak valid untuk metrik selain Euclidean.

### InsightFace Pipeline (per-wajah, 12.715 embeddings dari 2.533 foto)

| Metode | NB | Clusters | Noise | Coverage | Silhouette |
|---|---|---|---|---|---|
| Baseline HDBSCAN | NB8 | 54 | 43.7% | 56.2% | 0.4530 |
| **UMAP + HDBSCAN** | **NB9** | **95** | **0.7%** | **99.3%** | **0.9041** |
| Angular Distance | NB10 | 90 | 19.9% | 80.1% | 0.2573 |
| CGA Augmentation | NB12 | 54 | 43.6% | 56.4% | 0.4547 |
| NT-CGA | NB13 | 348 | 19.5% | 80.5% | 0.3005 |

### CLIP Pipeline (per-foto, 2.533 embeddings)

| Metode | NB | Clusters | Noise | Coverage | Silhouette |
|---|---|---|---|---|---|
| Baseline HDBSCAN (euclidean≡cosine) | NB16 | 2 | 12.6% | 87.45% | 0.2107 |
| **UMAP + HDBSCAN (best)** | **NB16** | **52** | **25.9%** | **74.14%** | **0.6467** |

> **Catatan**: InsightFace mengkluster berdasarkan *identitas wajah*, CLIP mengkluster berdasarkan *konten foto* (scene, aktivitas, suasana). Perbandingan antar pipeline bersifat indikatif karena perbedaan granularitas.

---

## Instalasi

```bash
git clone https://github.com/adenurchalisa/Automatic-Photo-Clustering-System-Optimization-HDBSCAN.git
cd Automatic-Photo-Clustering-System-Optimization-HDBSCAN

pip install -r requirements.txt
```

Untuk CLIP (diinstal langsung dari GitHub):
```bash
pip install git+https://github.com/openai/CLIP.git
```

---

## Struktur Repository

```
.
├── notebooks/
│   ├── 1_Eksperimen_HDBSCAN_hyperparameter.ipynb
│   ├── 2_Eksperimen_HDBSCAN_hyperparameter.ipynb
│   ├── 3_EDA_Baseline_Clustering.ipynb
│   ├── 4_Fokus_Hyperparameter.ipynb
│   ├── 5_Granular_Hyperparameter.ipynb
│   ├── 6_Distance_Metric_Compare.ipynb
│   ├── 8_Re_Tuning_Correlation.ipynb
│   ├── 9_UMAP_HDBSCAN_Pipeline.ipynb
│   ├── 10_Angular_SoftClustering.ipynb
│   ├── 11_Noise_Composition_Analysis.ipynb
│   ├── 12_CGA_Augmentation.ipynb
│   ├── 13_CGA_NoiseSingleton.ipynb
│   ├── 14_Final_Evaluation.ipynb
│   ├── 15_CLIP_Feature_Extraction.ipynb
│   └── 16_CLIP_HDBSCAN_Clustering.ipynb
├── src/
│   └── feature_extraction.ipynb
├── requirements.txt
└── README.md
```

---

## Dataset

- **Jumlah foto**: 2.533 foto dokumentasi
- **Foto dengan wajah**: 2.365 foto (93.4%)
- **Foto tanpa wajah**: 168 foto (6.6%)
- **Total face embeddings**: 12.715 (dari InsightFace)
- **Sumber**: Dataset foto dokumentasi kegiatan kampus UIN Alauddin Makassar

---

## Teknologi

| Komponen | Tools |
|---|---|
| Face embedding | InsightFace `buffalo_l` (512-dim) |
| Photo embedding | OpenAI CLIP `ViT-L/14` (768-dim) |
| Clustering | HDBSCAN |
| Dimensionality reduction | UMAP |
| Augmentasi | Gaussian noise (feature-space) |
| Evaluasi | Silhouette Score, Davies-Bouldin Index, Coverage |
| Environment | Google Colab (GPU) |

---

## Penulis

**Ade Nurchalisa**
Universitas Islam Negeri (UIN) Alauddin Makassar
