"""
Semua hyperparameter dan konstanta.
Nilai-nilai ini berasal dari hasil eksperimen NB05 (FAISS + HDBSCAN).

Konfigurasi terbaik (Final NB05):
  Coverage Rate : 92.36%
  Silhouette    : 0.3673
  n_clusters    : 144
"""

# InsightFace
FACE_MODEL_NAME    = "buffalo_l"    # Model InsightFace untuk deteksi + embedding
FACE_DET_SIZE      = (640, 640)     # Ukuran input face detection
FACE_DET_THRESHOLD = 0.5            # Confidence threshold deteksi wajah

# HDBSCAN — dari hasil eksperimen NB05 (Final)
# UMAP dihapus: direct HDBSCAN pada L2-normalized embeddings lebih stabil
HDBSCAN_MIN_CLUSTER_SIZE         = 50      # Minimum anggota per cluster
HDBSCAN_MIN_SAMPLES              = 5       # Kontrol konservatisme noise
HDBSCAN_CLUSTER_SELECTION_METHOD = "eom"   # "eom" atau "leaf"
HDBSCAN_METRIC                   = "euclidean"  # equiv. cosine karena embedding sudah L2-normalized

# App limits
MAX_PHOTOS_UPLOAD = 200                            # Batas upload untuk free tier
SUPPORTED_FORMATS = [".jpg", ".jpeg", ".png"]
TEMP_DIR          = "/tmp/facecluster"             # Direktori temporer

# UI
FACE_PADDING        = 0.1
MAX_CLUSTER_PREVIEW = 18
MAX_NOISE_PREVIEW   = 12
