
def main():
    from ultralytics import YOLO

    # Define the path to the YAML configuration file
    yaml_file = 'Datasets/Helmet/data.yaml'

    # Load the YOLO model
    model = YOLO('yolov8n.pt')

    # Train the model
    model.train(
        data=yaml_file,
        epochs=50,
        batch=8,
        imgsz=640,
        save=True,
        name='Helmet_yolov8(batch8)',
    )

    print("Training started...")

if __name__ == '__main__':

    main()



# # yolo task=segment mode=train model=yolov8n-seg.pt data=data.yaml epochs=50 imgsz=640 (for segmentation)
# #yolo export model=best.pt format=onnx
# #pip install onnx onnx-tf
# #onnx-tf convert -i best.onnx -o tf_model

