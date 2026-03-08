"""
Halaman upload: pilih foto dari file atau Google Drive.
"""

import streamlit as st

from src.config import MAX_PHOTOS_UPLOAD, SUPPORTED_FORMATS
from src.drive_handler import download_from_drive
from src.utils import save_uploaded_files


def render():
    st.header("📁 Upload Foto")
    st.caption(f"Maksimal {MAX_PHOTOS_UPLOAD} foto · Format: JPG, JPEG, PNG · Bisa upload ZIP")

    tab1, tab2 = st.tabs(["Upload File", "Google Drive Link"])

    with tab1:
        uploaded_files = st.file_uploader(
            "Pilih foto atau file ZIP",
            type=["jpg", "jpeg", "png", "zip"],
            accept_multiple_files=True,
            help="Drag & drop atau klik untuk memilih foto",
        )

        if uploaded_files:
            st.info(f"{len(uploaded_files)} file dipilih")
            if st.button("🔄 Proses Foto", type="primary", key="btn_upload"):
                with st.spinner("Menyimpan file..."):
                    photo_paths = save_uploaded_files(uploaded_files)
                    st.session_state.photos = photo_paths
                    st.session_state.page = "processing"
                    st.rerun()

    with tab2:
        drive_link = st.text_input(
            "Paste link Google Drive folder",
            placeholder="https://drive.google.com/drive/folders/...",
        )

        if drive_link:
            if st.button("🔄 Download & Proses", type="primary", key="btn_drive"):
                with st.spinner("Mengunduh dari Google Drive..."):
                    photo_paths, error = download_from_drive(drive_link)
                    if error:
                        st.error(error)
                    elif not photo_paths:
                        st.warning("Tidak ada foto yang ditemukan di link tersebut")
                    else:
                        st.success(f"{len(photo_paths)} foto berhasil diunduh")
                        st.session_state.photos = photo_paths
                        st.session_state.page = "processing"
                        st.rerun()
