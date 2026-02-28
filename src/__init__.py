"""
Thesis: Sistem Pengelompokan Foto Otomatis dan Penanganan Kondisi Few-Shot 
Menggunakan ALgoritma HDBSCAN dan Augmentasi Data Generatif

Author: Ade Nurchalisa
University: UIN Alauddin Makassar
"""

from .feature_extraction import FaceExtractor, extract_embeddings
from .distance_metrics import compute_distance_matrix, correlation_distance
from .clustering import run_hdbscan_clustering, evaluate_clustering
from .augmentation import apply_cga
from .utils import load_embeddings, save_embeddings

__version__ = "1.0.0"
__author__ = "Ade Nurchalisa"
