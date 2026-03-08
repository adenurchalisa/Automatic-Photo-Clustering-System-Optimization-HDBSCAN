"""
Entry point aplikasi FaceCluster.
Mengatur navigasi antar halaman menggunakan st.session_state.
"""

import streamlit as st

# Konfigurasi halaman — HARUS di baris pertama
st.set_page_config(
    page_title="FaceCluster",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session state initialization
if "page" not in st.session_state:
    st.session_state.page = "overview"
if "photos" not in st.session_state:
    st.session_state.photos = None          # List of uploaded photo paths
if "embeddings" not in st.session_state:
    st.session_state.embeddings = None      # Dict: {photo_path: [(face_idx, bbox, embedding), ...]}
if "clusters" not in st.session_state:
    st.session_state.clusters = None        # Dict: {cluster_id: [photo_paths]}
if "face_crops" not in st.session_state:
    st.session_state.face_crops = None      # Dict: {cluster_id: [cropped_face_images]}
if "cluster_labels" not in st.session_state:
    st.session_state.cluster_labels = None  # Array dari HDBSCAN labels

# Sidebar navigasi
from components.sidebar import render_sidebar
render_sidebar()

# Router halaman
from components.page_overview import render as overview
from components.page_upload import render as upload
from components.page_processing import render as processing
from components.page_results import render as results

pages = {
    "overview": overview,
    "upload": upload,
    "processing": processing,
    "results": results,
}

pages[st.session_state.page]()
