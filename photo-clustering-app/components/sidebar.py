"""
Sidebar: navigasi antar halaman dan info status.
"""

import streamlit as st


def render_sidebar():
    with st.sidebar:
        # Branding
        st.markdown("""
        <div style="text-align:center; padding:1.5rem 0 1.25rem;">
            <div style="font-size:2.8rem; margin-bottom:0.25rem;">📸</div>
            <div style="font-size:1.35rem; font-weight:800; letter-spacing:-0.02em;">FaceCluster</div>
            <div style="font-size:0.72rem; opacity:0.65; margin-top:0.2rem; font-weight:400;">
                Pengelompokan Foto Otomatis
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            '<div style="height:1px;background:rgba(255,255,255,0.18);margin-bottom:1rem;"></div>',
            unsafe_allow_html=True,
        )

        pages = {
            "overview":   ("🏠", "Beranda"),
            "upload":     ("📁", "Upload Foto"),
            "processing": ("⚙️", "Proses"),
            "results":    ("✨", "Hasil"),
        }

        for key, (icon, label) in pages.items():
            is_active = st.session_state.page == key
            if st.button(
                f"{icon}  {label}",
                key=f"nav_{key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.page = key
                st.rerun()

        st.markdown(
            '<div style="height:1px;background:rgba(255,255,255,0.18);margin:1rem 0;"></div>',
            unsafe_allow_html=True,
        )

        # Status info
        photos  = st.session_state.get("photos")
        clusters = st.session_state.get("clusters")
        metrics  = st.session_state.get("metrics")

        if photos:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.14);border-radius:12px;
                        padding:0.8rem 1rem;margin-bottom:0.6rem;
                        border:1px solid rgba(255,255,255,0.12);">
                <div style="font-size:0.7rem;opacity:0.75;font-weight:500;
                            text-transform:uppercase;letter-spacing:0.05em;
                            margin-bottom:0.2rem;">📷 Foto Dimuat</div>
                <div style="font-size:1.2rem;font-weight:800;">{len(photos)}</div>
                <div style="font-size:0.72rem;opacity:0.65;">foto siap diproses</div>
            </div>
            """, unsafe_allow_html=True)

        if clusters and metrics:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.14);border-radius:12px;
                        padding:0.8rem 1rem;border:1px solid rgba(255,255,255,0.12);">
                <div style="font-size:0.7rem;opacity:0.75;font-weight:500;
                            text-transform:uppercase;letter-spacing:0.05em;
                            margin-bottom:0.2rem;">👥 Hasil Clustering</div>
                <div style="font-size:1.2rem;font-weight:800;">{len(clusters)} cluster</div>
                <div style="font-size:0.72rem;opacity:0.65;">
                    {metrics.get('coverage_pct', 0)}% coverage
                </div>
            </div>
            """, unsafe_allow_html=True)
