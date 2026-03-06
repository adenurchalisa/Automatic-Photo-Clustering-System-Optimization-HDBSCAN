import os
import shutil
import tempfile

import gradio as gr
import numpy as np

from pipeline.input_handler import extract_images, validate_images
from pipeline.face_detector import FaceDetector
from pipeline.clusterer import cluster_embeddings, summarize
from pipeline.exporter import export_clusters, build_gallery

UPLOAD_DIR = tempfile.mkdtemp(prefix="fca_upload_")
OUTPUT_DIR = os.path.join(tempfile.gettempdir(), "fca_output")

detector = None  # lazy init


def get_detector():
    global detector
    if detector is None:
        detector = FaceDetector()
    return detector


def run_pipeline(files, min_cluster_size, min_samples, progress=gr.Progress()):
    if not files:
        return [], None, "No files uploaded."

    # --- 1. Input ---
    progress(0, desc="Extracting images…")
    upload_dir = tempfile.mkdtemp(prefix="fca_upload_")
    image_paths = extract_images(files, upload_dir)
    image_paths = validate_images(image_paths)

    if not image_paths:
        return [], None, "No valid images found."

    # --- 2. Face Detection ---
    progress(0.1, desc="Loading face detector…")
    det = get_detector()

    def det_progress(done, total):
        progress(0.1 + 0.6 * done / total, desc=f"Detecting faces… {done}/{total}")

    embeddings, sources = det.detect_batch(image_paths, progress_cb=det_progress)

    if len(embeddings) == 0:
        return [], None, "No faces detected in the uploaded images."

    # --- 3. Clustering ---
    progress(0.75, desc="Clustering faces…")
    labels = cluster_embeddings(
        embeddings,
        min_cluster_size=int(min_cluster_size),
        min_samples=int(min_samples),
    )

    stats = summarize(labels)

    # --- 4. Export ---
    progress(0.9, desc="Exporting results…")
    zip_path = export_clusters(sources, labels, OUTPUT_DIR)
    gallery_items = build_gallery(sources, labels)

    progress(1.0, desc="Done!")

    summary = (
        f"**Faces detected:** {stats['n_faces']}  \n"
        f"**Clusters found:** {stats['n_clusters']}  \n"
        f"**Noise / unassigned:** {stats['n_noise']}"
    )

    return gallery_items, zip_path, summary


with gr.Blocks(title="Face Clustering App") as demo:
    gr.Markdown("# Face Clustering App\nUpload photos → detect faces → cluster by identity.")

    with gr.Row():
        with gr.Column(scale=2):
            file_input = gr.File(
                label="Upload images or a ZIP file",
                file_count="multiple",
                file_types=["image", ".zip"],
            )
            with gr.Row():
                min_cluster_size_slider = gr.Slider(
                    minimum=2, maximum=20, value=2, step=1,
                    label="Min cluster size"
                )
                min_samples_slider = gr.Slider(
                    minimum=1, maximum=10, value=1, step=1,
                    label="Min samples (HDBSCAN)"
                )
            run_btn = gr.Button("Run Clustering", variant="primary")

        with gr.Column(scale=3):
            summary_md = gr.Markdown("Results will appear here.")
            gallery = gr.Gallery(
                label="Clustered Faces",
                columns=4,
                height="auto",
                object_fit="cover",
            )
            download_btn = gr.File(label="Download ZIP", interactive=False)

    run_btn.click(
        fn=run_pipeline,
        inputs=[file_input, min_cluster_size_slider, min_samples_slider],
        outputs=[gallery, download_btn, summary_md],
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
