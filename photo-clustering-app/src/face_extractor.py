"""
Modul untuk deteksi wajah dan ekstraksi face embedding.
Menggunakan InsightFace buffalo_l (512-dim ArcFace embeddings).

Fungsi utama:
- load_model(): Load InsightFace, cache dengan st.cache_resource
- extract_faces(image_path): Return list of (bbox, embedding, cropped_face)
- process_all_photos(photo_paths, progress_callback): Proses batch foto
"""

import cv2
import numpy as np
import streamlit as st
from insightface.app import FaceAnalysis

from src.config import FACE_DET_SIZE, FACE_DET_THRESHOLD, FACE_MODEL_NAME


@st.cache_resource
def load_model():
    """
    Load InsightFace model. Cache agar tidak download ulang tiap session.
    Return: FaceAnalysis object yang sudah di-prepare
    """
    app = FaceAnalysis(name=FACE_MODEL_NAME, providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=0, det_size=FACE_DET_SIZE)
    return app


def extract_faces(image_path, model=None):
    """
    Deteksi semua wajah di satu foto dan ekstrak embedding masing-masing.

    Args:
        image_path: Path ke file foto
        model: FaceAnalysis object (jika None, akan load otomatis)

    Returns:
        List of dict, masing-masing berisi:
        {
            "bbox": [x1, y1, x2, y2],        # Bounding box wajah
            "embedding": np.array (512-dim),   # Face embedding
            "crop": np.array (RGB image),      # Cropped face image
            "det_score": float,                # Detection confidence
            "source_photo": str                # Path foto asal
        }
    """
    if model is None:
        model = load_model()

    img = cv2.imread(image_path)
    if img is None:
        return []

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = model.get(img_rgb)

    results = []
    for face in faces:
        if face.det_score < FACE_DET_THRESHOLD:
            continue

        bbox = face.bbox.astype(int)
        x1, y1, x2, y2 = bbox

        # Crop wajah dengan padding
        h, w = img_rgb.shape[:2]
        pad = int(max(x2 - x1, y2 - y1) * 0.1)
        x1 = max(0, x1 - pad)
        y1 = max(0, y1 - pad)
        x2 = min(w, x2 + pad)
        y2 = min(h, y2 + pad)
        crop = img_rgb[y1:y2, x1:x2]

        results.append({
            "bbox": bbox.tolist(),
            "embedding": face.embedding,
            "crop": crop,
            "det_score": float(face.det_score),
            "source_photo": image_path,
        })

    return results


def process_all_photos(photo_paths, progress_callback=None):
    """
    Proses semua foto: deteksi wajah dan ekstrak embedding.

    Args:
        photo_paths: List of photo file paths
        progress_callback: Callable(current, total, message) untuk update progress

    Returns:
        all_faces: List of face dicts (dari extract_faces)
        stats: Dict dengan statistik {total_photos, photos_with_faces, total_faces}
    """
    model = load_model()
    all_faces = []
    photos_with_faces = 0

    for i, path in enumerate(photo_paths):
        if progress_callback:
            progress_callback(i + 1, len(photo_paths), f"Mendeteksi wajah: {i+1}/{len(photo_paths)}")

        faces = extract_faces(path, model)
        if faces:
            photos_with_faces += 1
        all_faces.extend(faces)

    stats = {
        "total_photos": len(photo_paths),
        "photos_with_faces": photos_with_faces,
        "total_faces": len(all_faces),
    }

    return all_faces, stats
