"""
Halaman processing: jalankan pipeline dan tampilkan progress.
"""

import streamlit as st

from src.pipeline import run_full_pipeline


def render():
    st.header("⏳ Memproses Foto...")

    photos = st.session_state.get("photos")
    if not photos:
        st.warning("Tidak ada foto untuk diproses. Silakan upload terlebih dahulu.")
        if st.button("← Kembali ke Upload"):
            st.session_state.page = "upload"
            st.rerun()
        return

    st.info(f"Memproses {len(photos)} foto...")
    progress_placeholder = st.empty()

    success = run_full_pipeline(photos, progress_placeholder)

    if success:
        metrics = st.session_state.get("metrics", {})
        face_stats = st.session_state.get("face_stats", {})

        st.success("Pengelompokan selesai!")

        # Tampilkan ringkasan
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Foto", face_stats.get("total_photos", 0))
        col2.metric("Wajah Terdeteksi", face_stats.get("total_faces", 0))
        col3.metric("Cluster", metrics.get("n_clusters", 0))
        col4.metric("Coverage", f"{metrics.get('coverage_pct', 0)}%")

        if st.button("📊 Lihat Hasil", type="primary", use_container_width=True):
            st.session_state.page = "results"
            st.rerun()
    else:
        st.error("Tidak ada wajah yang berhasil dideteksi dalam foto yang diupload.")
        if st.button("← Coba Lagi"):
            st.session_state.page = "upload"
            st.rerun()
