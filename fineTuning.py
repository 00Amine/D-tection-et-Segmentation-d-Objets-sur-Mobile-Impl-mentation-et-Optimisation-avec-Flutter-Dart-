import multiprocessing

def main():
    from ultralytics import YOLO

    # Path to the correct 4-class YAML file (must match model class structure)
    yaml_file = 'Datasets/HelmetAug/data.yaml'

    # Load the pretrained 4-class YOLOv8 model
    model = YOLO('runs/detect/Helmet_yolov8(batch8)/weights/best.pt')

    # Fine-tune the model on the new data
    model.train(
        data=yaml_file,
        epochs=50,
        batch=16,
        imgsz=640,
        save=True,
        name='Finetuning_yolov8',
    )

    print("Training started...")

if __name__ == '__main__':
    main()
