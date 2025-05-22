import os


def rename_images(folder_path, base_name="morocco"):
    """
    Renames all image files in a folder to a specified base name with sequential numbers.
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']

    try:
        files = os.listdir(folder_path)
    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
        return
    except PermissionError:
        print(f"Error: Permission denied to access '{folder_path}'.")
        return

    image_files = [f for f in files if os.path.splitext(f)[1].lower() in image_extensions]

    if not image_files:
        print("No image files found in the folder.")
        return

    print(f"Found {len(image_files)} image files to rename.")

    image_files.sort()

    for i, filename in enumerate(image_files, start=1):
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        new_name = f"{base_name}{i}{ext}"

        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)

        if os.path.exists(new_path):
            print(f"Warning: {new_name} already exists. Skipping {filename}.")
            continue

        try:
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_name}")
        except OSError as e:
            print(f"Error renaming {filename}: {e}")

    print("Renaming complete.")


if __name__ == "__main__":
    # Hardcoded folder path for your dataset
    folder_path = r"C:\Users\moham\PycharmProjects\projet_pfa\Datasets\helmet_nohelmet_ds"
    rename_images(folder_path, base_name="morocco")
