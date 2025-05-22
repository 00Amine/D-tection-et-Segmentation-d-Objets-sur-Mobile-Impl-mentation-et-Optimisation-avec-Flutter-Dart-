def main():
    from ultralytics import YOLO

    # Load each model
    models = [
        YOLO("runs/detect/Finetuning_yolov8/weights/best.pt"),
        YOLO("runs/detect/Helmet_yolov8/weights/best.pt"),
        YOLO("runs/detect/Helmet_yolov8(batch8)/weights/best.pt"),
        YOLO("runs/detect/HelmetAug_yolov8/weights/best.pt"),
        YOLO("runs/detect/HelmetAug_yolov8(batch4)/weights/best.pt"),
        YOLO("runs/detect/HelmetAug_yolov8(batch8)/weights/best.pt"),

    ]

    # Evaluate on the same test set
    for i, model in enumerate(models, 1):
        metrics = model.val(data="Datasets/HelmetAug/data.yaml", split='val')
        print(f"Model {i} -> mAP50: {metrics.box.map50:.4f}, mAP50-95: {metrics.box.map:.4f}")
if __name__ == '__main__':

    main()
