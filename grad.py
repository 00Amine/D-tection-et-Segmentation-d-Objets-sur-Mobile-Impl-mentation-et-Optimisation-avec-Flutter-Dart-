import gradio as gr
from ultralytics import YOLO
import cv2
import tempfile
from collections import Counter

# Load your YOLOv8 model
model = YOLO("runs/detect/HelmetAug_yolov8/weights/best.pt")


# 1. Image Prediction Function
def predict_image(img):
    results = model(img)[0]
    annotated = results.plot()

    # Extract classes
    names = model.names
    detected_classes = [names[int(cls)] for cls in results.boxes.cls]
    counts = Counter(detected_classes)
    summary = "\n".join(f"{cls}: {cnt}" for cls, cnt in counts.items())

    return annotated, summary


# 2. Video Prediction Function
def predict_video(video_path):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame)[0]
        annotated = results.plot()
        out.write(annotated)

    cap.release()
    out.release()
    return out_path


# 3. Gradio UI
with gr.Blocks(theme=gr.themes.Base(), title="Helmet & Rider Detection App") as demo:
    gr.Markdown(
        "<h1 style='text-align: center;'>🛡️ Helmet, Rider & Plate Nº Detection</h1>"
        "<p style='text-align: center; font-size: 16px;'>Powered by YOLOv8 - Real-time Safety Compliance Detection</p>"
    )

    with gr.Tab("🖼️ Image"):
        gr.Markdown("### 📸 Upload an image to detect:")
        with gr.Row():
            img_input = gr.Image(type="numpy", label="", show_label=False)
            img_button = gr.Button("🚀 Detect", scale=1)
        with gr.Row():
            img_output = gr.Image(label="📍 Detection Result", elem_classes="box")
            img_stats = gr.HighlightedText(label="🎯 Detected Classes Count", combine_adjacent=True)


        def predict_image(img):
            results = model(img)[0]
            annotated = results.plot()

            names = model.names
            detected_classes = [names[int(cls)] for cls in results.boxes.cls]
            counts = Counter(detected_classes)
            summary = [(cls, f"{cls}: {cnt}") for cls, cnt in counts.items()]
            return annotated, summary


        img_button.click(fn=predict_image, inputs=img_input, outputs=[img_output, img_stats])

    with gr.Tab("🎞️ Video"):
        gr.Markdown("### 🎥 Upload a video to analyze:")
        with gr.Row():
            video_input = gr.Video(label="", show_label=False)
            video_button = gr.Button("🚀 Process Video", scale=1)
        with gr.Row():
            video_output = gr.Video(label="🔍 Detection Output")

        video_button.click(fn=predict_video, inputs=video_input, outputs=video_output)

    gr.Markdown("<p style='text-align: center; font-size: 14px; color: grey;'>© 2025 MGSI | YOLOv8 powered</p>")

demo.launch()
