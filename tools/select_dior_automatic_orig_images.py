import os
import shutil
from pathlib import Path

from tqdm import tqdm

image_folder = Path("datasets/DIOR/JPEGImages-trainval")

reference_folder = Path("datasets/DIOR_automatic_label/image_lable")
softlink_folder = Path("datasets/DIOR_automatic_label/orig_images")

if softlink_folder.exists():
    shutil.rmtree(softlink_folder)

softlink_folder.mkdir(parents=True, exist_ok=True)

# Get the list of image files
image_files = list(reference_folder.glob("*.jpg"))

# Create a progress bar
progress_bar = tqdm(total=len(image_files), unit="image")

for image_file in reference_folder.glob("*.jpg"):
    progress_bar.update(1)
    # retrieve the image_file name in the image_folder
    image_file_name = image_file.stem
    # create the soft link in softlink_folder
    orig_path = image_folder / f"{image_file_name}.jpg"
    orig_full_path = orig_path.resolve()
    softlink_path = softlink_folder / f"{image_file_name}.jpg"
    softlink_full_path = softlink_path.resolve()
    # create the soft link using os
    os.symlink(orig_full_path, softlink_full_path)

    print("--------------------------------------------------")
progress_bar.close()