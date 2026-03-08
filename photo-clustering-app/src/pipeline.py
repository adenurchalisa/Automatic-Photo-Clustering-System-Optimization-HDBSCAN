"""
Orchestrator: menjalankan seluruh pipeline dari foto input sampai cluster output.
Dipanggil dari page_processing.py.

Fungsi utama:
- run_full_pipeline(photo_paths, progress_placeholder): Jalankan semua step
"""

import streamlit as st

from src.clustering import run_clustering_pipeline
from src.face_extractor import process_all_photos


def run_full_pipeline(photo_paths, progress_placeholder):
    """
    Jalankan pipeline lengkap dan update progress di UI.

    Args:
        photo_paths: List of photo file paths
        progress_placeholder: st.empty() untuk menampilkan progress

    Menyimpan hasil ke st.session_state:
        - st.session_state.clusters
        - st.session_state.noise_faces
        - st.session_state.metrics
        - st.session_state.face_stats
    """
    progress_bar = progress_placeholder.progress(0, text="Memulai...")

    # STEP 1: Face Detection & Embedding
    def face_progress(current, total, msg):
        pct = int((current / total) * 50)  # 0-50%
        progress_bar.progress(pct, text=msg)

    all_faces, face_stats = process_all_photos(photo_paths, face_progress)
    st.session_state.face_stats = face_stats

    if not all_faces:
        progress_bar.progress(100, text="Tidak ada wajah terdeteksi!")
        return False

    # STEP 2 & 3: UMAP + HDBSCAN
    def cluster_progress(current, total, msg):
        pct = 50 + int((current / total) * 50)  # 50-100%
        progress_bar.progress(pct, text=msg)

    clusters, noise_faces, metrics = run_clustering_pipeline(all_faces, cluster_progress)

    # Simpan ke session state
    st.session_state.clusters = clusters
    st.session_state.noise_faces = noise_faces
    st.session_state.metrics = metrics

    progress_bar.progress(100, text="Selesai!")
    return True
