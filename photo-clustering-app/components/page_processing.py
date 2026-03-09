"""
Halaman processing: jalankan pipeline dan tampilkan progress.
"""

import streamlit as st

from src.pipeline import run_full_pipeline


def render():
    photos = st.session_state.get("photos")

    if not photos:
        st.markdown("""
        <div style="text-align:center;padding:4rem 1rem;">
            <div style="font-size:3.5rem;margin-bottom:1rem;">📭</div>
            <div style="font-size:1.2rem;font-weight:800;color:#1E293B;margin-bottom:0.5rem;">
                Belum Ada Foto
            </div>
            <div style="color:#64748B;font-size:0.9rem;">
                Silakan upload foto terlebih dahulu
            </div>
        </div>
        """, unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            if st.button("← Upload Foto", use_container_width=True):
                st.session_state.page = "upload"
                st.rerun()
        return

    st.markdown(f"""
    <div style="margin-bottom:1.75rem;">
        <h2 style="font-weight:800;color:#1E293B;margin-bottom:0.2rem;">⚙️ Memproses Foto</h2>
        <p style="color:#64748B;font-size:0.9rem;margin:0;">
            Mendeteksi dan mengelompokkan wajah dari {len(photos)} foto
        </p>
    </div>
    """, unsafe_allow_html=True)

    progress_placeholder = st.empty()
    success = run_full_pipeline(photos, progress_placeholder)

    if success:
        metrics    = st.session_state.get("metrics", {})
        face_stats = st.session_state.get("face_stats", {})

        st.markdown("""
        <div style="background:linear-gradient(135deg,#ECFDF5,#D1FAE5);
                    border-radius:16px;padding:1.5rem;text-align:center;
                    border:1px solid #A7F3D0;margin-bottom:1.75rem;">
            <div style="font-size:2.2rem;margin-bottom:0.5rem;">🎉</div>
            <div style="font-size:1.15rem;font-weight:800;color:#065F46;">
                Pengelompokan Selesai!
            </div>
            <div style="font-size:0.85rem;color:#047857;margin-top:0.25rem;">
                Semua wajah berhasil diidentifikasi dan dikelompokkan
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        stats_data = [
            (col1, face_stats.get("total_photos", 0),  "Total Foto",        "🖼️"),
            (col2, face_stats.get("total_faces", 0),   "Wajah Terdeteksi",  "🔍"),
            (col3, metrics.get("n_clusters", 0),        "Cluster Terbentuk", "👥"),
            (col4, f"{metrics.get('coverage_pct', 0)}%","Coverage",          "✅"),
        ]
        for col, value, label, icon in stats_data:
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size:1.4rem;margin-bottom:0.4rem;">{icon}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='margin:1.5rem 0;'></div>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("✨ Lihat Hasil Clustering", type="primary", use_container_width=True):
                st.session_state.page = "results"
                st.rerun()

    else:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#FEF2F2,#FEE2E2);
                    border-radius:16px;padding:1.5rem;text-align:center;
                    border:1px solid #FECACA;margin-bottom:1.5rem;">
            <div style="font-size:2.2rem;margin-bottom:0.5rem;">😔</div>
            <div style="font-size:1.1rem;font-weight:800;color:#7F1D1D;">
                Tidak Ada Wajah Terdeteksi
            </div>
            <div style="font-size:0.85rem;color:#991B1B;margin-top:0.25rem;">
                Pastikan foto mengandung wajah yang cukup jelas dan tidak terlalu kecil
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            if st.button("← Coba Lagi", use_container_width=True):
                st.session_state.page = "upload"
                st.rerun()
