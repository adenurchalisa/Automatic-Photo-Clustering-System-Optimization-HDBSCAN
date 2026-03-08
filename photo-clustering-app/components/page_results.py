"""
Halaman hasil: gallery per cluster, pilih cluster, download.
Ini halaman utama yang dilihat user setelah proses selesai.
"""

import streamlit as st

from src.utils import create_cluster_zip, numpy_to_pil


def render():
    clusters = st.session_state.get("clusters")
    metrics = st.session_state.get("metrics")
    noise_faces = st.session_state.get("noise_faces", [])

    if not clusters:
        st.warning("Belum ada hasil clustering.")
        if st.button("← Upload Foto"):
            st.session_state.page = "upload"
            st.rerun()
        return

    # Header metrics
    st.header("📊 Hasil Pengelompokan")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Cluster", metrics["n_clusters"])
    col2.metric("Coverage", f"{metrics['coverage_pct']}%")
    col3.metric("Noise", f"{metrics['noise_pct']}%")
    col4.metric("Silhouette", metrics.get("silhouette", "N/A"))

    st.markdown("---")

    # Multi-select download
    cluster_ids = list(clusters.keys())
    cluster_labels = [f"Cluster {cid + 1} ({len(clusters[cid])} wajah)" for cid in cluster_ids]

    selected_labels = st.multiselect(
        "Pilih cluster untuk download:",
        options=cluster_labels,
        help="Pilih satu atau lebih cluster, lalu klik tombol download",
    )

    # Map selected labels back to IDs
    selected_ids = []
    for label in selected_labels:
        idx = cluster_labels.index(label)
        selected_ids.append(cluster_ids[idx])

    if selected_ids:
        zip_buffer = create_cluster_zip(clusters, selected_ids)
        st.download_button(
            label=f"↓ Download {len(selected_ids)} Cluster (ZIP)",
            data=zip_buffer,
            file_name="facecluster_results.zip",
            mime="application/zip",
            type="primary",
        )

    st.markdown("---")

    # Gallery per cluster
    for cid in cluster_ids:
        faces = clusters[cid]
        n_photos = len(set(f["source_photo"] for f in faces))

        with st.expander(f"👤 Cluster {cid + 1} — {len(faces)} wajah dari {n_photos} foto", expanded=False):

            # Per-cluster download button
            single_zip = create_cluster_zip(clusters, [cid])
            st.download_button(
                label=f"↓ Download Cluster {cid + 1}",
                data=single_zip,
                file_name=f"cluster_{cid + 1}.zip",
                mime="application/zip",
                key=f"dl_{cid}",
            )

            # Tampilkan face crops dalam grid
            cols = st.columns(6)
            for i, face in enumerate(faces[:18]):  # Max 18 preview
                with cols[i % 6]:
                    pil_img = numpy_to_pil(face["crop"])
                    st.image(pil_img, use_container_width=True)

            if len(faces) > 18:
                st.caption(f"Menampilkan 18 dari {len(faces)} wajah")

    # Noise section
    if noise_faces:
        with st.expander(f"🔇 Noise — {len(noise_faces)} wajah tidak terkelompok"):
            cols = st.columns(6)
            for i, face in enumerate(noise_faces[:12]):
                with cols[i % 6]:
                    pil_img = numpy_to_pil(face["crop"])
                    st.image(pil_img, use_container_width=True)

    # Reset button
    st.markdown("---")
    if st.button("🔄 Proses Foto Baru"):
        for key in ["photos", "clusters", "noise_faces", "metrics", "face_stats"]:
            st.session_state[key] = None
        st.session_state.page = "upload"
        st.rerun()
