import os
import shutil
import zipfile
from pathlib import Path
import numpy as np


def export_clusters(
    image_sources: list[str],
    labels: np.ndarray,
    output_dir: str,
) -> str:
    """
    Copy images into per-cluster sub-folders and zip them.

    Folder structure inside the zip:
        cluster_00/photo1.jpg
        cluster_01/photo2.jpg
        noise/photo3.jpg     ← label == -1

    Returns path to the created zip file.
    """
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for src_path, label in zip(image_sources, labels):
        folder_name = f"cluster_{label:02d}" if label >= 0 else "noise"
        dest_dir = os.path.join(output_dir, folder_name)
        os.makedirs(dest_dir, exist_ok=True)

        filename = Path(src_path).name
        dest_path = os.path.join(dest_dir, filename)
        # Avoid overwriting same filename from different source dirs
        if os.path.exists(dest_path):
            stem = Path(filename).stem
            suffix = Path(filename).suffix
            dest_path = os.path.join(dest_dir, f"{stem}_{hash(src_path) % 10000}{suffix}")

        shutil.copy2(src_path, dest_path)

    zip_path = output_dir.rstrip("/\\") + ".zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(output_dir):
            for fname in files:
                abs_path = os.path.join(root, fname)
                arcname = os.path.relpath(abs_path, os.path.dirname(output_dir))
                zf.write(abs_path, arcname)

    return zip_path


def build_gallery(
    image_sources: list[str],
    labels: np.ndarray,
) -> list[tuple[str, str]]:
    """
    Returns a list of (image_path, caption) pairs for gr.Gallery.
    """
    gallery = []
    for src, label in zip(image_sources, labels):
        caption = f"Cluster {label}" if label >= 0 else "Noise"
        gallery.append((src, caption))
    return gallery
