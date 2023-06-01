import os
import json
from PIL import Image
from tqdm import tqdm

# Path to dataset folder
dataset_folder = 'datasets/remote_sensing/RS_images'

# Path to annotations folder
annotations_folder = 'datasets/remote_sensing/annotations'


# Function to rename folder and format its name in camel case
def rename_folder(folder_path):
    words = folder_path.split('/')
    last_folder = words[-1]
    words[-1] = last_folder[0].lower() + last_folder[1:].replace(' ', '_')
    new_path = '/'.join(words)
    os.rename(folder_path, new_path)
    return new_path


# Rename folders and format their names in camel case
for folder in os.listdir(dataset_folder):
    folder_path = os.path.join(dataset_folder, folder)
    if os.path.isdir(folder_path):
        rename_folder(folder_path)

# Generate category_id and mapping
category2id = {}
id2category = {}
for idx, folder in enumerate(os.listdir(dataset_folder)):
    folder_path = os.path.join(dataset_folder, folder)
    if os.path.isdir(folder_path):
        category2id[folder] = idx
        id2category[idx] = folder

# Save mapping to JSON files
with open(os.path.join(annotations_folder, 'category2id.json'), 'w') as f:
    json.dump(category2id, f)

with open(os.path.join(annotations_folder, 'id2category.json'), 'w') as f:
    json.dump(id2category, f)

# Generate image_info
image_info = []
img_counter = 0
cats = []
for folder in tqdm(os.listdir(dataset_folder)):
    folder_path = os.path.join(dataset_folder, folder)
    img_counter_within_folder = 0
    if os.path.isdir(folder_path):
        # get the number of images in the folder
        category = folder
        num_images = len([name for name in os.listdir(folder_path) if name.endswith('.jpg')])
        cat_info = {"id": category2id[folder], "name": category, "image_count": num_images}
        cats.append(cat_info)
        for img_file in os.listdir(folder_path):
            if not img_file.endswith('.jpg'):
                continue
            img_path = os.path.join(folder, img_file)
            try:
                img_width, img_height = Image.open(os.path.join(folder_path, img_file)).size
                img_counter += 1
                img_counter_within_folder += 1
            except Exception as e:
                print("Error in file: " + img_path)
                # delete file
                os.remove(os.path.join(folder_path, img_file))
                print(e)
                continue

            # new_name = str(img_counter_within_folder).zfill(8) + '.jpg'
            new_name = str(category2id[folder]) + '_' + str(img_counter_within_folder).zfill(8) + '.jpg'
            os.rename(os.path.join(folder_path, img_file), os.path.join(folder_path, new_name))
            img_path = os.path.join(folder, new_name)

            img_info = {"id": img_counter, "file_name": img_path, "pos_category_ids": [category2id[folder]], "width": img_width, "height": img_height}
            image_info.append(img_info)

# for i in image_info:
#     if i['pos_category_ids'][0] ==117:
#         print(i['file_name'])

with open(os.path.join(annotations_folder, 'image_info.json'), 'w') as f:
    out = {'categories': cats, 'images': image_info, 'annotations': []}
    f = json.dump(out, f)
