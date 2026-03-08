"""
Modul untuk download foto dari Google Drive link.
Mendukung folder link dan individual file links.

Fungsi utama:
- download_from_drive(link, output_dir): Download semua foto dari link
"""

import os
import re

import gdown

from src.config import MAX_PHOTOS_UPLOAD, SUPPORTED_FORMATS, TEMP_DIR


def extract_drive_id(link):
    """
    Ekstrak folder/file ID dari berbagai format Google Drive link.

    Supports:
    - https://drive.google.com/drive/folders/FOLDER_ID
    - https://drive.google.com/file/d/FILE_ID/view
    - https://drive.google.com/open?id=ID

    Returns: (id, type) dimana type = "folder" atau "file"
    """
    # Folder link
    folder_match = re.search(r'/folders/([a-zA-Z0-9_-]+)', link)
    if folder_match:
        return folder_match.group(1), "folder"

    # File link
    file_match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', link)
    if file_match:
        return file_match.group(1), "file"

    # Generic id parameter
    id_match = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', link)
    if id_match:
        return id_match.group(1), "file"

    return None, None


def download_from_drive(link, output_dir=None):
    """
    Download foto dari Google Drive link.

    Args:
        link: Google Drive URL (folder atau file)
        output_dir: Direktori output (default: TEMP_DIR/drive_photos)

    Returns:
        photo_paths: List of downloaded photo file paths
        error: Error message string jika gagal, None jika sukses
    """
    if output_dir is None:
        output_dir = os.path.join(TEMP_DIR, "drive_photos")

    os.makedirs(output_dir, exist_ok=True)

    drive_id, link_type = extract_drive_id(link)
    if drive_id is None:
        return [], "Link Google Drive tidak valid"

    try:
        if link_type == "folder":
            url = f"https://drive.google.com/drive/folders/{drive_id}"
            gdown.download_folder(url, output=output_dir, quiet=True)
        else:
            url = f"https://drive.google.com/uc?id={drive_id}"
            gdown.download(url, output=output_dir, quiet=True)
    except Exception as e:
        return [], f"Gagal download: {str(e)}"

    # Kumpulkan semua foto yang valid
    photo_paths = []
    for root, dirs, files in os.walk(output_dir):
        for f in files:
            if any(f.lower().endswith(ext) for ext in SUPPORTED_FORMATS):
                photo_paths.append(os.path.join(root, f))

    if len(photo_paths) > MAX_PHOTOS_UPLOAD:
        photo_paths = photo_paths[:MAX_PHOTOS_UPLOAD]

    return photo_paths, None
