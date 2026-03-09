"""
Halaman hasil: gallery per cluster, pilih cluster, download.
"""

import streamlit as st

from src.utils import create_cluster_zip, numpy_to_pil


def render():
    clusters    = st.session_state.get("clusters")
    metrics     = st.session_state.get("metrics")
    noise_faces = st.session_state.get("noise_faces", [])

    if not clusters:
        st.markdown("""
        <div style="text-align:center;padding:4rem 1rem;">
            <div style="font-size:3.5rem;margin-bottom:1rem;">🔍</div>
            <div style="font-size:1.2rem;font-weight:800;color:#1E293B;margin-bottom:0.5rem;">
                Belum Ada Hasil
            </div>
            <div style="color:#64748B;font-size:0.9rem;">
                Proses foto terlebih dahulu untuk melihat hasil clustering
            </div>
        </div>
        """, unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            if st.button("← Upload Foto", use_container_width=True):
                st.session_state.page = "upload"
                st.rerun()
        return

    # ── Header ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:1.75rem;">
        <h2 style="font-weight:800;color:#1E293B;margin-bottom:0.2rem;">✨ Hasil Clustering</h2>
        <p style="color:#64748B;font-size:0.9rem;margin:0;">
            Wajah yang terdeteksi telah dikelompokkan secara otomatis
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Metric cards ───────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    metric_data = [
        (col1, metrics["n_clusters"],              "Cluster",    "👥"),
        (col2, f"{metrics['coverage_pct']}%",      "Coverage",   "✅"),
        (col3, f"{metrics['noise_pct']}%",         "Noise",      "🔇"),
        (col4, metrics.get("silhouette") or "—",   "Silhouette", "📊"),
    ]
    for col, value, label, icon in metric_data:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size:1.5rem;margin-bottom:0.4rem;">{icon}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ── Download section ───────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-size:1rem;font-weight:700;color:#1E293B;margin-bottom:0.75rem;">
        📥 Download Cluster
    </div>
    """, unsafe_allow_html=True)

    cluster_ids    = list(clusters.keys())
    cluster_labels = [f"Cluster {cid + 1}  ({len(clusters[cid])} wajah)" for cid in cluster_ids]

    selected_labels = st.multiselect(
        "Pilih cluster yang ingin didownload:",
        options=cluster_labels,
        placeholder="Pilih satu atau lebih cluster...",
        label_visibility="collapsed",
    )
    selected_ids = [cluster_ids[cluster_labels.index(l)] for l in selected_labels]

    if selected_ids:
        zip_buffer = create_cluster_zip(clusters, selected_ids)
        st.download_button(
            label=f"⬇️  Download {len(selected_ids)} Cluster (ZIP)",
            data=zip_buffer,
            file_name="facecluster_results.zip",
            mime="application/zip",
            use_container_width=True,
        )

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ── Gallery ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-size:1rem;font-weight:700;color:#1E293B;margin-bottom:0.75rem;">
        👤 Gallery Cluster
    </div>
    """, unsafe_allow_html=True)

    for cid in cluster_ids:
        faces    = clusters[cid]
        n_photos = len(set(f["source_photo"] for f in faces))

        with st.expander(
            f"Cluster {cid + 1}  ·  {len(faces)} wajah  ·  {n_photos} foto",
            expanded=False,
        ):
            col_dl, col_info = st.columns([1, 3])
            with col_dl:
                single_zip = create_cluster_zip(clusters, [cid])
                st.download_button(
                    label="⬇️ Download",
                    data=single_zip,
                    file_name=f"cluster_{cid + 1}.zip",
                    mime="application/zip",
                    key=f"dl_{cid}",
                    use_container_width=True,
                )
            with col_info:
                st.markdown(f"""
                <div style="padding:0.5rem 0;color:#64748B;font-size:0.82rem;line-height:1.6;">
                    {len(faces)} wajah terdeteksi dari <strong>{n_photos}</strong> foto berbeda
                </div>
                """, unsafe_allow_html=True)

            cols = st.columns(6)
            for i, face in enumerate(faces[:18]):
                with cols[i % 6]:
                    st.image(numpy_to_pil(face["crop"]), use_container_width=True)

            if len(faces) > 18:
                st.caption(f"Menampilkan 18 dari {len(faces)} wajah")

    # ── Noise section ──────────────────────────────────────────────────────────
    if noise_faces:
        with st.expander(f"🔇 Tidak Terkelompok  ·  {len(noise_faces)} wajah", expanded=False):
            st.markdown("""
            <div style="background:#FFF7ED;border-radius:10px;padding:0.6rem 0.9rem;
                        margin-bottom:0.75rem;font-size:0.8rem;color:#92400E;">
                Wajah-wajah ini tidak memiliki kemiripan yang cukup dengan cluster manapun
            </div>
            """, unsafe_allow_html=True)
            cols = st.columns(6)
            for i, face in enumerate(noise_faces[:12]):
                with cols[i % 6]:
                    st.image(numpy_to_pil(face["crop"]), use_container_width=True)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # ── Reset ──────────────────────────────────────────────────────────────────
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("🔄 Proses Foto Baru", use_container_width=True):
            for key in ["photos", "clusters", "noise_faces", "metrics", "face_stats"]:
                st.session_state[key] = None
            st.session_state.page = "upload"
            st.rerun()
