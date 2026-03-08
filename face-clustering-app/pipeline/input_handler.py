import os
import zipfile
import shutil
from pathlib import Path
from PIL import Image

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def extract_images(source, upload_dir: str) -> list[str]:
    """
    Accepts either:
    - A list of image file paths (from gr.File with multiple=True)
    - A single zip file path
    Returns a list of absolute image paths.
    """
    os.makedirs(upload_dir, exist_ok=True)

    image_paths = []

    if isinstance(source, list):
        for f in source:
            path = Path(f.name if hasattr(f, "name") else f)
            if path.suffix.lower() in SUPPORTED_EXTENSIONS:
                dest = Path(upload_dir) / path.name
                shutil.copy(str(path), str(dest))
                image_paths.append(str(dest))
    elif isinstance(source, str) and source.endswith(".zip"):
        with zipfile.ZipFile(source, "r") as z:
            z.extractall(upload_dir)
        for root, _, files in os.walk(upload_dir):
            for fname in files:
                if Path(fname).suffix.lower() in SUPPORTED_EXTENSIONS:
                    image_paths.append(os.path.join(root, fname))
    else:
        path = Path(source.name if hasattr(source, "name") else source)
        if path.suffix.lower() in SUPPORTED_EXTENSIONS:
            dest = Path(upload_dir) / path.name
            shutil.copy(str(path), str(dest))
            image_paths.append(str(dest))

    return sorted(image_paths)


def validate_images(image_paths: list[str]) -> list[str]:
    """Filter out corrupt or unreadable images."""
    valid = []
    for p in image_paths:
        try:
            with Image.open(p) as img:
                img.verify()
            valid.append(p)
        except Exception:
            pass
    return valid
