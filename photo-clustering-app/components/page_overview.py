"""
Halaman pertama: nama aplikasi, deskripsi, dan cara menggunakan.
"""

import streamlit as st


def render():
    st.markdown("---")

    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center'>📸 FaceCluster</h1>", unsafe_allow_html=True)
        st.markdown(
            "<p style='text-align:center; color:gray'>Sistem Pengelompokan Foto Otomatis Berbasis Wajah</p>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Deskripsi
    st.markdown("""
    **FaceCluster** secara otomatis mengelompokkan foto-foto dokumentasi berdasarkan
    identitas wajah. Upload koleksi foto Anda, dan sistem akan mendeteksi setiap wajah,
    mengenali siapa yang sama, lalu mengelompokkannya — tanpa perlu pelabelan manual.
    """)

    # Cara menggunakan
    st.subheader("Cara Menggunakan")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Step 1** — Upload foto atau paste link Google Drive")
        st.markdown("**Step 2** — Tunggu sistem mendeteksi & mengelompokkan wajah")
    with col2:
        st.markdown("**Step 3** — Lihat hasil — setiap cluster = 1 orang")
        st.markdown("**Step 4** — Pilih cluster yang diinginkan, lalu download")

    # Teknologi
    st.subheader("Teknologi")
    tech_cols = st.columns(4)
    techs = [
        ("InsightFace", "Face Detection & Embedding"),
        ("UMAP", "Dimensionality Reduction"),
        ("HDBSCAN", "Density-based Clustering"),
        ("Streamlit", "Web Interface"),
    ]
    for col, (name, desc) in zip(tech_cols, techs):
        with col:
            st.metric(label=name, value=desc)

    st.markdown("---")

    # CTA
    if st.button("🚀 Mulai Pengelompokan", type="primary", use_container_width=True):
        st.session_state.page = "upload"
        st.rerun()

    st.caption("Skripsi — Ade Nurchalisa · UIN Alauddin Makassar · 2026")
