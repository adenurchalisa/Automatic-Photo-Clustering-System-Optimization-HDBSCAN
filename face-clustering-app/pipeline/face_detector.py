import numpy as np
import cv2
import insightface
from insightface.app import FaceAnalysis


class FaceDetector:
    def __init__(self, det_size=(640, 640), ctx_id=0):
        self.app = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"],
        )
        self.app.prepare(ctx_id=ctx_id, det_size=det_size)

    def detect(self, image_path: str) -> list[np.ndarray]:
        """
        Returns list of 512-d face embeddings detected in the image.
        Returns empty list if no face found.
        """
        img = cv2.imread(image_path)
        if img is None:
            return []
        faces = self.app.get(img)
        embeddings = []
        for face in faces:
            if face.embedding is not None:
                embeddings.append(face.embedding)
        return embeddings

    def detect_batch(self, image_paths: list[str], progress_cb=None):
        """
        Returns:
            embeddings: np.ndarray of shape (N, 512)
            sources   : list of image paths, one per embedding
        """
        all_embeddings = []
        all_sources = []
        for i, path in enumerate(image_paths):
            embs = self.detect(path)
            for emb in embs:
                all_embeddings.append(emb)
                all_sources.append(path)
            if progress_cb:
                progress_cb(i + 1, len(image_paths))

        if not all_embeddings:
            return np.empty((0, 512)), []

        return np.vstack(all_embeddings), all_sources
