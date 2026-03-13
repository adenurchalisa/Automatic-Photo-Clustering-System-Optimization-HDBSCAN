"""
Modul clustering: HDBSCAN langsung pada L2-normalized embeddings.
Pipeline dari eksperimen NB05 (hasil final: Coverage 92.36%, Silhouette 0.3673).

Konfigurasi final (NB05):
  HDBSCAN: min_cluster_size=50, min_samples=5, metric=euclidean, method=eom
  UMAP dihapus — direct HDBSCAN lebih stabil dan tidak menciptakan artefak kompresi.

Fungsi utama:
- cluster_faces(embeddings): HDBSCAN clustering pada embedding
- run_clustering_pipeline(all_faces): End-to-end dari embedding ke cluster assignment
"""

import logging

import hdbscan
import numpy as np
from sklearn.metrics import silhouette_score

from src.config import (
    HDBSCAN_CLUSTER_SELECTION_METHOD,
    HDBSCAN_MIN_CLUSTER_SIZE,
    HDBSCAN_MIN_SAMPLES,
    HDBSCAN_METRIC,
)

logger = logging.getLogger(__name__)


def cluster_faces(embeddings):
    """
    Cluster L2-normalized embeddings langsung dengan HDBSCAN.
    Tidak pakai UMAP — sesuai hasil eksperimen NB05.

    Args:
        embeddings: np.array shape (n_faces, 512), sudah L2-normalized

    Returns:
        labels: np.array of cluster labels (-1 = noise)
        metrics: Dict {n_clusters, n_noise, noise_pct, coverage_pct, silhouette}
    """
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=HDBSCAN_MIN_CLUSTER_SIZE,
        min_samples=HDBSCAN_MIN_SAMPLES,
        cluster_selection_method=HDBSCAN_CLUSTER_SELECTION_METHOD,
        metric=HDBSCAN_METRIC,
        approx_min_span_tree=True,
        core_dist_n_jobs=-1,
    )
    labels = clusterer.fit_predict(embeddings)

    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = int((labels == -1).sum())
    total = len(labels)

    metrics = {
        "n_clusters": n_clusters,
        "n_noise": n_noise,
        "noise_pct": round(n_noise / total * 100, 1),
        "coverage_pct": round((total - n_noise) / total * 100, 1),
        "silhouette": None,
    }

    # Silhouette hanya bisa dihitung jika ada > 1 cluster dan tidak semua noise
    clustered_mask = labels >= 0
    if n_clusters > 1 and clustered_mask.sum() > n_clusters:
        try:
            sample_size = min(2000, int(clustered_mask.sum()))
            rng = np.random.default_rng(42)
            sample_idx = rng.choice(np.where(clustered_mask)[0], size=sample_size, replace=False)
            metrics["silhouette"] = round(
                float(silhouette_score(embeddings[sample_idx], labels[sample_idx])),
                4,
            )
        except Exception as e:
            logger.warning("Silhouette gagal: %s", e)

    return labels, metrics


def run_clustering_pipeline(all_faces, progress_callback=None):
    """
    Pipeline lengkap dari face data ke cluster assignment.

    Args:
        all_faces: List of face dicts (dari face_extractor.process_all_photos)
        progress_callback: Callable(current, total, message)

    Returns:
        clusters: Dict {cluster_id: [face_dicts]} — setiap cluster berisi list face
        noise_faces: List of face_dicts yang masuk noise
        metrics: Dict metrik evaluasi clustering
    """
    if progress_callback:
        progress_callback(1, 2, "Menyiapkan embeddings...")

    # Kumpulkan semua embedding
    embeddings = np.array([f["embedding"] for f in all_faces], dtype=np.float32)

    # Pastikan L2-normalized (InsightFace buffalo_l sudah normalized, ini safeguard)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1, norms)
    embeddings = embeddings / norms

    if progress_callback:
        progress_callback(2, 2, "Mengelompokkan wajah (HDBSCAN)...")

    # HDBSCAN langsung pada embeddings
    labels, metrics = cluster_faces(embeddings)

    # Organize ke dalam clusters
    clusters = {}
    noise_faces = []

    for face, label in zip(all_faces, labels):
        face["cluster_id"] = int(label)
        if label == -1:
            noise_faces.append(face)
        else:
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(face)

    # Sort clusters by size (terbesar dulu) dan re-index dari 0
    clusters = dict(sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True))
    clusters = {i: v for i, (_, v) in enumerate(clusters.items())}

    logger.info(
        "Clustering selesai: %d cluster, coverage %.1f%%, noise %.1f%%",
        metrics["n_clusters"], metrics["coverage_pct"], metrics["noise_pct"],
    )
    return clusters, noise_faces, metrics
