"""
Modul clustering: UMAP dimensionality reduction + HDBSCAN.
Pipeline dari eksperimen NB9 (hasil terbaik: Coverage 99.3%, Silhouette 0.9041).

Konfigurasi terbaik (Best by Coverage Rate):
  UMAP: n_components=30, n_neighbors=30, metric=cosine, min_dist=0.0
  HDBSCAN: min_cluster_size=20, min_samples=20, method=eom

Fungsi utama:
- reduce_dimensions(embeddings): UMAP reduction
- cluster_faces(reduced_embeddings): HDBSCAN clustering
- run_clustering_pipeline(all_faces): End-to-end dari embedding ke cluster assignment
"""

import hdbscan
import numpy as np
import umap
from sklearn.metrics import silhouette_score

from src.config import (
    HDBSCAN_CLUSTER_SELECTION_METHOD,
    HDBSCAN_MIN_CLUSTER_SIZE,
    HDBSCAN_MIN_SAMPLES,
    UMAP_METRIC,
    UMAP_MIN_DIST,
    UMAP_N_COMPONENTS,
    UMAP_N_NEIGHBORS,
    UMAP_RANDOM_STATE,
)


def reduce_dimensions(embeddings):
    """
    Reduksi dimensi embedding dari 512 → n_components menggunakan UMAP.

    Args:
        embeddings: np.array shape (n_faces, 512)

    Returns:
        reduced: np.array shape (n_faces, n_components)
        reducer: fitted UMAP object (untuk transform data baru jika diperlukan)
    """
    reducer = umap.UMAP(
        n_components=UMAP_N_COMPONENTS,
        n_neighbors=UMAP_N_NEIGHBORS,
        min_dist=UMAP_MIN_DIST,
        metric=UMAP_METRIC,
        random_state=UMAP_RANDOM_STATE,
    )
    reduced = reducer.fit_transform(embeddings)
    return reduced, reducer


def cluster_faces(reduced_embeddings):
    """
    Clustering embedding yang sudah direduksi menggunakan HDBSCAN.

    Args:
        reduced_embeddings: np.array shape (n_faces, n_components)

    Returns:
        labels: np.array of cluster labels (-1 = noise)
        clusterer: fitted HDBSCAN object
        metrics: Dict {n_clusters, n_noise, noise_pct, coverage_pct, silhouette}
    """
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=HDBSCAN_MIN_CLUSTER_SIZE,
        min_samples=HDBSCAN_MIN_SAMPLES,
        cluster_selection_method=HDBSCAN_CLUSTER_SELECTION_METHOD,
    )
    labels = clusterer.fit_predict(reduced_embeddings)

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
        metrics["silhouette"] = round(
            silhouette_score(reduced_embeddings[clustered_mask], labels[clustered_mask]),
            4,
        )

    return labels, clusterer, metrics


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
        progress_callback(1, 3, "Mereduksi dimensi (UMAP)...")

    # Kumpulkan semua embedding
    embeddings = np.array([f["embedding"] for f in all_faces])

    # UMAP
    reduced, _ = reduce_dimensions(embeddings)

    if progress_callback:
        progress_callback(2, 3, "Mengelompokkan wajah (HDBSCAN)...")

    # HDBSCAN
    labels, _, metrics = cluster_faces(reduced)

    if progress_callback:
        progress_callback(3, 3, "Menyusun hasil...")

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

    # Sort clusters by size (terbesar dulu)
    clusters = dict(sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True))

    return clusters, noise_faces, metrics
