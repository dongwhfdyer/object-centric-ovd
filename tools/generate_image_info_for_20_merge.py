import csv
import json
import os
from pathlib import Path
import cv2

category2id = {}
id2category = {}

with open('tools/category_id_info.csv', encoding='utf-8-sig', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        label, value = row
        label = label.replace(' ', '_')
        value = int(value)
        category2id[label] = value
        id2category[value] = label

image_folder = Path("datasets/CLASS_20_merge")
img_counter = 0

category_info = {}
img_infos = []
# cat_info = {"id": category2id[folder], "name": category, "image_count": num_images}
for image_file in image_folder.glob("*"):
    cat_id = int(image_file.stem.split('_')[0])
    file_name = image_file.name
    if cat_id not in category_info:
        category_info[cat_id] = 1
    else:
        category_info[cat_id] += 1

    img_width = cv2.imread(str(image_file)).shape[1]
    img_height = cv2.imread(str(image_file)).shape[0]

    img_info = {"id": img_counter, "file_name": file_name, "pos_category_ids": [cat_id], "width": img_width, "height": img_height}
    img_counter += 1
    img_infos.append(img_info)

# convert the category_info to list
category_info_list = []
for cat_id, img_count in category_info.items():
    cat_info = {"id": cat_id, "name": id2category[cat_id], "image_count": img_count}
    category_info_list.append(cat_info)

with open(os.path.join('datasets/DIOR_20_Merge_labled/20_merge_image_info.json'), 'w') as f:
    out = {'categories': category_info_list, 'images': img_infos, 'annotations': []}
    f = json.dump(out, f)
