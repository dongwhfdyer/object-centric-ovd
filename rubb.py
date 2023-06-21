import os

images_dir = 'datasets/remote_sensing/RS_images'
image_files = []

# Walk through the directory tree and get a list of all image files
for dirpath, dirnames, filenames in os.walk(images_dir):
    for filename in filenames:
        if filename.endswith('.jpg'):
            image_path = os.path.join(dirpath, filename)
            image_files.append(image_path)


# randomly sample 100 images and move them to one folder
folder = 'rubb/RS_images_sampled'
if not os.path.exists(folder):
    os.makedirs(folder)

import random
import shutil

num_samples = 100
sampled_image_files = random.sample(image_files, num_samples)

for img_file in sampled_image_files:
    shutil.copy(img_file, folder)



