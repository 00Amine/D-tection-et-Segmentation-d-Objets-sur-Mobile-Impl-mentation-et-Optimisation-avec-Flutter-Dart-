import os
import hashlib
from PIL import Image
import imagehash

# Define the folders to clean
folders = [
    "Datasets/HelmetAug/train/images",
    "Datasets/HelmetAug/val/images"
]

# Function to find exact duplicates using MD5
def find_duplicates(folder_path):
    hashes = {}
    duplicates = []

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            if file_hash in hashes:
                duplicates.append(filepath)
            else:
                hashes[file_hash] = filepath
    return duplicates

# Function to find near-duplicates using perceptual hashing (pHash)
def find_near_duplicates(folder_path, hash_size=8, threshold=5):
    hashes = {}
    duplicates = []

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        try:
            img = Image.open(filepath)
            img_hash = imagehash.phash(img, hash_size=hash_size)
            for saved_hash in hashes:
                if abs(img_hash - saved_hash) <= threshold:
                    duplicates.append(filepath)
                    break
            else:
                hashes[img_hash] = filepath
        except:
            continue
    return duplicates

# === Process each folder ===
for folder in folders:
    print(f"\n--- Processing folder: {folder} ---")

    # Remove exact duplicates
    exact_dups = find_duplicates(folder)
    for dup in exact_dups:
        print(f"[EXACT] Duplicate found and removed: {dup}")
        os.remove(dup)

    # Remove near duplicates
    near_dups = find_near_duplicates(folder)
    for dup in near_dups:
        print(f"[NEAR] Duplicate found and removed: {dup}")
        os.remove(dup)
