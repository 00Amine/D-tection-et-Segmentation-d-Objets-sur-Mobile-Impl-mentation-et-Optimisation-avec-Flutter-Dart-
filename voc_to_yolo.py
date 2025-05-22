import os
import xml.etree.ElementTree as ET

# CONFIGURE THIS
IMG_DIR = "Datasets/construction_helmet dataset/images"
ANNOTATIONS_DIR = "Datasets/construction_helmet dataset/annotations"
YOLO_LABELS_DIR = os.path.join(ANNOTATIONS_DIR, "labels")
CLASSES = ["helmet", "no_helmet"]  # Update this list with your actual classes

os.makedirs(YOLO_LABELS_DIR, exist_ok=True)

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    return (x * dw, y * dh, w * dw, h * dh)

for xml_file in os.listdir(ANNOTATIONS_DIR):
    if not xml_file.endswith(".xml"):
        continue

    tree = ET.parse(os.path.join(ANNOTATIONS_DIR, xml_file))
    root = tree.getroot()

    size = root.find("size")
    if size is None:
        print(f"Warning: <size> tag missing in {xml_file}, skipping this file.")
        continue

    w = int(size.find("width").text)
    h = int(size.find("height").text)

    txt_file = os.path.join(YOLO_LABELS_DIR, os.path.splitext(xml_file)[0] + ".txt")

    with open(txt_file, "w") as f:
        object_found = False
        for obj in root.findall("object"):
            cls = obj.find("name").text
            if cls not in CLASSES:
                continue

            cls_id = CLASSES.index(cls)
            xmlbox = obj.find("bndbox")

            if xmlbox is not None:
                b = (
                    float(xmlbox.find("xmin").text),
                    float(xmlbox.find("xmax").text),
                    float(xmlbox.find("ymin").text),
                    float(xmlbox.find("ymax").text)
                )

                if b[0] >= b[1] or b[2] >= b[3]:
                    print(f"Skipping invalid bbox in {xml_file}: {b}")
                    continue

                bb = convert((w, h), b)
                f.write(f"{cls_id} {' '.join([str(round(a, 6)) for a in bb])}\n")
                object_found = True
            else:
                print(f"Warning: No <bndbox> found for object '{cls}' in {xml_file}. Using default bounding box.")
                b = (w / 4, 3 * w / 4, h / 4, 3 * h / 4)
                bb = convert((w, h), b)
                f.write(f"{cls_id} {' '.join([str(round(a, 6)) for a in bb])}\n")
                object_found = True

        if not object_found:
            print(f"Warning: No valid objects found in {xml_file}, txt file may be empty.")

print("✅ VOC to YOLO conversion done.")
