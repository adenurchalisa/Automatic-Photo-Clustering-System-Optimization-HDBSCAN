import numpy as np
from sklearn.preprocessing import normalize
import hdbscan


def cluster_embeddings(
    embeddings: np.ndarray,
    min_cluster_size: int = 2,
    min_samples: int = 1,
    metric: str = "euclidean",
) -> np.ndarray:
    """
    Cluster face embeddings with HDBSCAN.

    Args:
        embeddings   : (N, 512) float array of L2-normalized face embeddings
        min_cluster_size: minimum faces per cluster
        min_samples  : HDBSCAN min_samples parameter
        metric       : distance metric ('euclidean' recommended after L2 norm)

    Returns:
        labels: (N,) int array; -1 = noise / unassigned
    """
    if len(embeddings) == 0:
        return np.array([], dtype=int)

    # L2-normalize so cosine distance ≈ euclidean distance
    normed = normalize(embeddings, norm="l2")

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric=metric,
        core_dist_n_jobs=1,
    )
    labels = clusterer.fit_predict(normed)
    return labels


def summarize(labels: np.ndarray) -> dict:
    """Return basic stats about the clustering result."""
    unique = set(labels.tolist())
    n_clusters = len(unique - {-1})
    n_noise = int((labels == -1).sum())
    return {
        "n_faces": len(labels),
        "n_clusters": n_clusters,
        "n_noise": n_noise,
    }
