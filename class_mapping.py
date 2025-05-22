import os

# Remapping: new_class_id -> original_class_id
id_map = {
    0: 3,  # Plate -> Plate N°
    1: 0,  # WithHelmet -> With Helmet
    2: 1,  # WithoutHelmet -> Without Helmet
}

label_dirs = [
    "Datasets/PlateDetect/train/labels",
    "Datasets/PlateDetect/val/labels"
]

for label_dir in label_dirs:
    for file in os.listdir(label_dir):
        if file.endswith(".txt"):
            filepath = os.path.join(label_dir, file)
            with open(filepath, "r") as f:
                lines = f.readlines()

            new_lines = []
            for line in lines:
                parts = line.strip().split()
                class_id = int(parts[0])
                if class_id in id_map:
                    parts[0] = str(id_map[class_id])
                    new_lines.append(" ".join(parts))

            with open(filepath, "w") as f:
                f.write("\n".join(new_lines))
