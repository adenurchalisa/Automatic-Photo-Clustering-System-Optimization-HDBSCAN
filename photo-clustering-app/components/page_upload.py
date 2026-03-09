"""
Halaman upload: pilih foto dari file atau Google Drive.
"""

import streamlit as st

from src.config import MAX_PHOTOS_UPLOAD, SUPPORTED_FORMATS
from src.drive_handler import download_from_drive
from src.utils import save_uploaded_files


def render():
    st.markdown("""
    <div style="margin-bottom:1.75rem;">
        <h2 style="font-weight:800;color:#1E293B;margin-bottom:0.2rem;">📁 Upload Foto</h2>
        <p style="color:#64748B;font-size:0.9rem;margin:0;">
            Pilih foto atau file ZIP untuk mulai proses pengelompokan wajah
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📂 Upload dari Komputer", "🔗 Google Drive Link"])

    # ── Tab 1: Upload file ────────────────────────────────────────────────────
    with tab1:
        st.markdown(f"""
        <div style="background:#EEF2FF;border-radius:12px;padding:0.7rem 1rem;
                    margin-bottom:1.25rem;border-left:3px solid #4F46E5;">
            <span style="color:#4338CA;font-size:0.83rem;font-weight:500;">
                ℹ️ Maksimal <strong>{MAX_PHOTOS_UPLOAD} foto</strong>
                &nbsp;·&nbsp; Format: JPG, JPEG, PNG
                &nbsp;·&nbsp; ZIP didukung
            </span>
        </div>
        """, unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Drag & drop foto ke sini, atau klik untuk memilih",
            type=["jpg", "jpeg", "png", "zip"],
            accept_multiple_files=True,
            label_visibility="visible",
        )

        if uploaded_files:
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:1rem 1.25rem;
                        border:1px solid #C7D2FE;margin:1rem 0;
                        display:flex;align-items:center;gap:12px;">
                <span style="font-size:1.6rem;">✅</span>
                <div>
                    <div style="font-weight:700;color:#1E293B;font-size:0.95rem;">
                        {len(uploaded_files)} file dipilih
                    </div>
                    <div style="font-size:0.78rem;color:#64748B;margin-top:0.1rem;">
                        Siap untuk diproses
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🚀 Mulai Proses", type="primary", use_container_width=True, key="btn_upload"):
                with st.spinner("Menyimpan file..."):
                    photo_paths = save_uploaded_files(uploaded_files)
                    st.session_state.photos = photo_paths
                    st.session_state.page = "processing"
                    st.rerun()

    # ── Tab 2: Google Drive ───────────────────────────────────────────────────
    with tab2:
        st.markdown("""
        <div style="background:#FFF7ED;border-radius:12px;padding:0.7rem 1rem;
                    margin-bottom:1.25rem;border-left:3px solid #F59E0B;">
            <span style="color:#92400E;font-size:0.83rem;font-weight:500;">
                ⚠️ Foto dari Google Drive akan
                <strong>diunduh terlebih dahulu</strong> sebelum diproses
            </span>
        </div>
        """, unsafe_allow_html=True)

        drive_link = st.text_input(
            "Link Google Drive Folder",
            placeholder="https://drive.google.com/drive/folders/...",
        )

        if drive_link:
            if st.button("☁️ Download & Proses", type="primary", use_container_width=True, key="btn_drive"):
                with st.spinner("Mengunduh dari Google Drive..."):
                    photo_paths, error = download_from_drive(drive_link)
                    if error:
                        st.error(error)
                    elif not photo_paths:
                        st.warning("Tidak ada foto yang ditemukan di link tersebut.")
                    else:
                        st.success(f"✅ {len(photo_paths)} foto berhasil diunduh")
                        st.session_state.photos = photo_paths
                        st.session_state.page = "processing"
                        st.rerun()
