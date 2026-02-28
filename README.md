## 📋 Overview

This repository contains the complete experimental pipeline for my undergraduate thesis:

**"Sistem Pengelompokan Foto Otomatis dan Penanganan Kondisi Few-Shot Menggunakan Algoritma HDBSCAN dan Augmentasi Data Generatif"**

## 🎯 Research Questions

1. **RQ1**: Bagaimana merancang sistem pengelompokan otomatis yang efektif untuk mengatasi permasalahan data foto dokumentasi yang tidak terstruktur dan sulit dicari?

2. **RQ2**: Bagaimana mengatasi permasalahan kategori foto dengan jumlah sampel sangat sedikit (few-shot) yang menyebabkan algoritma clustering sulit membentuk cluster kecil atau cenderung menganggapnya sebagai noise?

## 🔬 Methodology

### Feature Extraction
- **Model**: InsightFace (buffalo_l)
- **Output**: 512-dimensional face embeddings

### Experiment 1: Distance Metric Comparison
- **Algorithm**: HDBSCAN
- **Metrics Tested**: Euclidean, QJSD, Cosine, Manhattan, Chebyshev, Minkowski, Correlation, Canberra
- **Evaluation**: Silhouette Score, Davies-Bouldin Index

### Experiment 2: CGA Augmentation
- **Method**: Cluster-based Generative Augmentation (feature-space)
- **Target**: Minority clusters and noise reduction

## 📊 Results Summary

| Experiment | Best Config | Silhouette | Clusters | Noise |
|------------|-------------|------------|----------|-------|
| Baseline (Euclidean) | mcs=20, ms=50 | 0.4432 | 44 | 69.3% |
| Exp 1 (Best Metric) | Correlation | 0.4432 | 64 | 36.3% |
| Exp 1.5 (Re-tuned) | mcs=15, ms=140 | 0.4862 | 28 | 70.3% |
| Exp 2 (CGA) | TBD | TBD | TBD | TBD |

## 🛠️ Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/thesis-face-clustering.git
cd thesis-face-clustering

# Install dependencies
pip install -r requirements.txt
```

## 📁 Project Structure

```
thesis-face-clustering/
├── notebooks/          # Jupyter/Colab notebooks
├── src/                # Source code modules
├── configs/            # Configuration files
├── results/            # Experiment results
└── docs/               # Documentation
```

## 🚀 Usage

### 1. Feature Extraction
```python
from src.feature_extraction import extract_embeddings

embeddings, metadata = extract_embeddings(
    input_folder='path/to/photos',
    output_path='embeddings_data.pkl'
)
```

### 2. Run Clustering
```python
from src.clustering import run_hdbscan_clustering

results = run_hdbscan_clustering(
    embeddings=embeddings,
    metric='correlation',
    min_cluster_size=15,
    min_samples=140
)
```


## 👤 Author

- **Name**: Ade Nurchalisa
- **University**: UIN Alauddin Makassar
