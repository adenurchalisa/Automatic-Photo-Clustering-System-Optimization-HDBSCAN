"""
Semua hyperparameter dan konstanta.
Nilai-nilai ini berasal dari hasil eksperimen NB9 (UMAP+HDBSCAN).

Konfigurasi terbaik (Best by Coverage Rate):
  Coverage Rate : 99.3%  (baseline: 56.2%)
  Silhouette    : 0.9041 (baseline: 0.4530)
  n_clusters    : 95
"""

# InsightFace
FACE_MODEL_NAME    = "buffalo_l"    # Model InsightFace untuk deteksi + embedding
FACE_DET_SIZE      = (640, 640)     # Ukuran input face detection
FACE_DET_THRESHOLD = 0.5            # Confidence threshold deteksi wajah

# UMAP — dari hasil eksperimen NB9 (Best Coverage Rate)
UMAP_N_COMPONENTS = 30              # 512-dim → 30-dim
UMAP_N_NEIGHBORS  = 30              # Ukuran lingkungan lokal
UMAP_MIN_DIST     = 0.0             # 0.0 untuk clustering (bukan visualisasi)
UMAP_METRIC       = "cosine"        # ArcFace embedding → cosine lebih tepat
UMAP_RANDOM_STATE = 42              # Reproducibility

# HDBSCAN — dari hasil eksperimen NB9 (Best Coverage Rate)
HDBSCAN_MIN_CLUSTER_SIZE         = 20    # Minimum anggota per cluster
HDBSCAN_MIN_SAMPLES              = 20    # Kontrol konservatisme noise
HDBSCAN_CLUSTER_SELECTION_METHOD = "eom" # "eom" atau "leaf"

# App limits
MAX_PHOTOS_UPLOAD = 200                            # Batas upload untuk free tier
SUPPORTED_FORMATS = [".jpg", ".jpeg", ".png"]
TEMP_DIR          = "/tmp/facecluster"             # Direktori temporer
