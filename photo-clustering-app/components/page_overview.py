"""
Halaman pertama: hero section, fitur, cara menggunakan, teknologi.
"""

import streamlit as st


def render():
    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">✨ Pengelompokan Wajah Otomatis</div>
        <div class="hero-title">📸 FaceCluster</div>
        <div class="hero-subtitle">
            Upload foto dokumentasimu — sistem akan mendeteksi,<br>
            mengenali, dan mengelompokkan setiap wajah secara otomatis.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Feature cards ─────────────────────────────────────────────────────────
    features = [
        ("🔍", "Deteksi Wajah",    "InsightFace mendeteksi setiap wajah dengan akurasi tinggi"),
        ("🧬", "Face Embedding",   "512-dim vector merepresentasikan identitas unik setiap wajah"),
        ("🗺️", "UMAP Reduction",   "Reduksi dimensi untuk mempersiapkan data clustering"),
        ("🎯", "HDBSCAN Cluster",  "Pengelompokan density-based tanpa perlu tentukan jumlah cluster"),
    ]

    cols = st.columns(4)
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <span class="feature-icon">{icon}</span>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ── Steps + Teknologi ─────────────────────────────────────────────────────
    col_left, col_right = st.columns([1.3, 1])

    with col_left:
        st.markdown("""
        <div style="font-size:1.05rem;font-weight:800;color:#1E293B;margin-bottom:1rem;">
            Cara Menggunakan
        </div>
        """, unsafe_allow_html=True)

        steps = [
            ("Upload",    "Pilih foto atau file ZIP dari komputer kamu"),
            ("Proses",    "Sistem mendeteksi wajah & menghitung embedding"),
            ("Cluster",   "UMAP + HDBSCAN mengelompokkan wajah yang sama"),
            ("Download",  "Pilih cluster yang diinginkan & unduh hasilnya"),
        ]
        for i, (title, desc) in enumerate(steps, 1):
            st.markdown(f"""
            <div class="step-card">
                <div class="step-number">{i}</div>
                <div class="step-text"><strong>{title}</strong> — {desc}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div style="font-size:1.05rem;font-weight:800;color:#1E293B;margin-bottom:1rem;">
            Teknologi
        </div>
        """, unsafe_allow_html=True)

        techs = [
            ("InsightFace", "Face Detection & Recognition"),
            ("UMAP",        "Dimensionality Reduction"),
            ("HDBSCAN",     "Density-based Clustering"),
            ("Streamlit",   "Web Interface"),
        ]
        for name, desc in techs:
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:0.9rem 1.1rem;
                        border:1px solid #E8ECFF;margin-bottom:0.5rem;
                        transition:border-color 0.2s;">
                <div style="font-weight:700;color:#1E293B;font-size:0.92rem;">{name}</div>
                <div style="font-size:0.78rem;color:#64748B;margin-top:0.15rem;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ── CTA ───────────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🚀 Mulai Sekarang", type="primary", use_container_width=True):
            st.session_state.page = "upload"
            st.rerun()

    st.markdown("""
    <div style="text-align:center;color:#CBD5E1;font-size:0.78rem;margin-top:1.5rem;">
        Skripsi — Ade Nurchalisa &nbsp;·&nbsp; UIN Alauddin Makassar &nbsp;·&nbsp; 2026
    </div>
    """, unsafe_allow_html=True)
