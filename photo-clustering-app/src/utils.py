"""
Fungsi utilitas: ZIP creation, image helpers, cleanup.

Fungsi utama:
- create_cluster_zip(clusters, selected_ids): Buat ZIP dari cluster terpilih
- save_uploaded_files(uploaded_files): Simpan file upload ke temp dir
- cleanup_temp(): Bersihkan file temporer
"""

import io
import os
import shutil
import zipfile

import numpy as np
from PIL import Image

from src.config import MAX_PHOTOS_UPLOAD, SUPPORTED_FORMATS, TEMP_DIR


def save_uploaded_files(uploaded_files):
    """
    Simpan file yang diupload user ke direktori temporer.

    Args:
        uploaded_files: List of Streamlit UploadedFile objects

    Returns:
        photo_paths: List of saved file paths
    """
    output_dir = os.path.join(TEMP_DIR, "uploads")
    os.makedirs(output_dir, exist_ok=True)

    photo_paths = []
    for f in uploaded_files:
        if any(f.name.lower().endswith(ext) for ext in SUPPORTED_FORMATS):
            path = os.path.join(output_dir, f.name)
            with open(path, "wb") as out:
                out.write(f.getbuffer())
            photo_paths.append(path)

        # Handle ZIP upload
        elif f.name.lower().endswith(".zip"):
            zip_bytes = io.BytesIO(f.getbuffer())
            with zipfile.ZipFile(zip_bytes, "r") as zf:
                for name in zf.namelist():
                    if any(name.lower().endswith(ext) for ext in SUPPORTED_FORMATS):
                        extracted_path = zf.extract(name, output_dir)
                        photo_paths.append(extracted_path)

    # Enforce limit
    if len(photo_paths) > MAX_PHOTOS_UPLOAD:
        photo_paths = photo_paths[:MAX_PHOTOS_UPLOAD]

    return photo_paths


def create_cluster_zip(clusters, selected_ids):
    """
    Buat ZIP file berisi foto-foto dari cluster yang dipilih.
    Struktur ZIP: Cluster_1/foto1.jpg, Cluster_2/foto2.jpg, ...

    Args:
        clusters: Dict {cluster_id: [face_dicts]}
        selected_ids: List/Set of cluster_ids yang ingin didownload

    Returns:
        zip_buffer: io.BytesIO object berisi ZIP file
    """
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for cid in selected_ids:
            if cid not in clusters:
                continue

            folder_name = f"Cluster_{cid + 1}"
            # Track unique photos (satu foto bisa punya banyak wajah)
            added_photos = set()

            for face in clusters[cid]:
                photo_path = face["source_photo"]
                if photo_path in added_photos:
                    continue
                added_photos.add(photo_path)

                filename = os.path.basename(photo_path)
                arcname = f"{folder_name}/{filename}"
                zf.write(photo_path, arcname)

    zip_buffer.seek(0)
    return zip_buffer


def numpy_to_pil(img_array):
    """Convert numpy array (RGB) ke PIL Image."""
    return Image.fromarray(img_array.astype(np.uint8))


def cleanup_temp():
    """Hapus semua file temporer."""
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
