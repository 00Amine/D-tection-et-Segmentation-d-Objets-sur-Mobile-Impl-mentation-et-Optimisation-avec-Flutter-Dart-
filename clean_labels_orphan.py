import os

base_path = 'Datasets/HelmetAug'
subsets = ['train', 'val']

for subset in subsets:
    image_folder = os.path.join(base_path, subset, 'images')
    label_folder = os.path.join(base_path, subset, 'labels')

    image_files = {
        os.path.splitext(f)[0]
        for f in os.listdir(image_folder)
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.jfif'))
    }

    for label_file in os.listdir(label_folder):
        label_name = os.path.splitext(label_file)[0]
        label_path = os.path.join(label_folder, label_file)

        # FIXED: This line must be indented to be inside the loop
        if label_name not in image_files:
            print(f"Deleting orphan label: {label_path}")
            os.remove(label_path)
