import os
import random
import shutil

# Set up paths
img_dir = 'Datasets/construction_helmet dataset/img'
label_dir = 'Datasets/construction_helmet dataset/labels'
train_img_dir = 'Datasets/construction_helmet dataset/train/images'
train_label_dir = 'Datasets/construction_helmet dataset/train/labels'
val_img_dir = 'Datasets/construction_helmet dataset/val/images'
val_label_dir = 'Datasets/construction_helmet dataset/val/labels'

# Create folders
for d in [train_img_dir, train_label_dir, val_img_dir, val_label_dir]:
    os.makedirs(d, exist_ok=True)

# List images
images = [f for f in os.listdir(img_dir) if f.endswith(('.jpg', '.png'))]
random.shuffle(images)
split_idx = int(len(images) * 0.8)

# Move files
for i, img in enumerate(images):
    label = img.rsplit('.', 1)[0] + '.txt'
    if i < split_idx:
        shutil.move(os.path.join(img_dir, img), os.path.join(train_img_dir, img))
        shutil.move(os.path.join(label_dir, label), os.path.join(train_label_dir, label))
    else:
        shutil.move(os.path.join(img_dir, img), os.path.join(val_img_dir, img))
        shutil.move(os.path.join(label_dir, label), os.path.join(val_label_dir, label))

print("Split completed.")
