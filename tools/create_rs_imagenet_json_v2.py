"""
This version has taken the dior datasets into account.
Dior datasets(object detection) have 20 classes. 15 classes are set as seen classes and 5 classes are set as unseen classes.
For this rs datasets(classification), all of them should be set as unseen classes. But due to the lack of groundtruth boundingbox,
we do not use the rs dataset for evaluation. We only use the rs dataset for training.

And there are some classes in rs dataset overlapping with dior dataset. So we have manually set the category_id for each class in rs dataset stored in `category2id.xlsx`.

One more thing: in dior dataset, there is one class called `train station`, while in rs dataset, there is one class called `railway station`.
So, we change the `railway station` to `train station` in rs dataset.

The general process in the following code:
1. Rename folders and format their names in camel case
2. Read `category2id.csv` and get the mapping from category to id
3. Rename the class `railway station` to `train station`.
4. Iterate over image folder, rename every image.
5. Save them to json file.
"""
import os
import json
from PIL import Image
from tqdm import tqdm
import csv

# Path to dataset folder
dataset_folder = 'datasets/remote_sensing/RS_images'

# Path to annotations folder
annotations_folder = 'datasets/remote_sensing/annotations'


# Function to rename folder and format its name in camel case
def rename_folder(folder_path):
    words = folder_path.split('/')
    last_folder = words[-1]
    if last_folder == 'railway_station':
        last_folder = 'train_station'
    words[-1] = last_folder[0].lower() + last_folder[1:].replace(' ', '_')
    new_path = '/'.join(words)
    os.rename(folder_path, new_path)
    return new_path


# Generate category_id and mapping
category2id = {}
id2category = {}

# Open the CSV file (replace with the path to your file)
with open('tools/category_id_info.csv', encoding='utf-8-sig', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        # remove the useless token

        label, value = row
        label = label.replace(' ', '_')
        value = int(value)
        category2id[label] = value
        id2category[value] = label

    # Rename folders and format their names in camel case
for folder in os.listdir(dataset_folder):
    folder_path = os.path.join(dataset_folder, folder)
    if os.path.isdir(folder_path):
        rename_folder(folder_path)

# Save mapping to JSON files
with open(os.path.join(annotations_folder, 'category2id.json'), 'w') as f:
    json.dump(category2id, f)

with open(os.path.join(annotations_folder, 'id2category.json'), 'w') as f:
    json.dump(id2category, f)

# Generate image_info
image_info = []
img_counter = 0
cats = []
indd = 0
for folder in tqdm(os.listdir(dataset_folder)):
    folder_path = os.path.join(dataset_folder, folder)
    if os.path.isdir(folder_path):
        img_counter_within_folder = 0
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
            except Exception as e:
                print("Error in file: " + img_path)
                # delete file
                os.remove(os.path.join(folder_path, img_file))
                print(e)
                continue
            img_counter += 1
            img_counter_within_folder += 1

            # new_name = str(img_counter_within_folder).zfill(8) + '.jpg'
            new_name = str(category2id[folder]) + '_' + str(img_counter_within_folder).zfill(8) + '.jpg'
            os.rename(os.path.join(folder_path, img_file), os.path.join(folder_path, new_name))  # todo: !!!!!!! critical error
            img_path = os.path.join(folder, new_name)

            img_info = {"id": img_counter, "file_name": img_path, "pos_category_ids": [category2id[folder]], "width": img_width, "height": img_height}
            image_info.append(img_info)

# for i in image_info:
#     if i['pos_category_ids'][0] ==117:
#         print(i['file_name'])

with open(os.path.join(annotations_folder, 'image_info.json'), 'w') as f:
    out = {'categories': cats, 'images': image_info, 'annotations': []}
    f = json.dump(out, f)
