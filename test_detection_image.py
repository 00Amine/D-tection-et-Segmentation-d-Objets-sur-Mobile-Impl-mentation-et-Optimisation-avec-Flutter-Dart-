from ultralytics import YOLO

model = YOLO('license_plate_detector.pt')
img_path = 'Detection/images/image2.jpeg'

results = model(img_path)[0]  # Access the first result


results.show()

