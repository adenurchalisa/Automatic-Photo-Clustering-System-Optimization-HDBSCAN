"""
Sidebar: navigasi antar halaman dan info status.
"""

import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.markdown("### 📸 FaceCluster")
        st.caption("Pengelompokan Foto Otomatis")

        st.markdown("---")

        # Navigasi
        pages = {
            "overview": "ℹ️ Overview",
            "upload": "📁 Upload",
            "processing": "⏳ Processing",
            "results": "📊 Hasil",
        }

        for key, label in pages.items():
            is_active = st.session_state.page == key
            if st.button(
                label,
                key=f"nav_{key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.page = key
                st.rerun()

        # Status info
        st.markdown("---")
        photos = st.session_state.get("photos")
        clusters = st.session_state.get("clusters")

        if photos:
            st.success(f"📷 {len(photos)} foto loaded")
        if clusters:
            st.success(f"👥 {len(clusters)} cluster terdeteksi")
