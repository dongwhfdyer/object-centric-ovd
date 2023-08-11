# img_info = {"id": img_counter, "file_name": img_path, "pos_category_ids": [category2id[folder]], "width": img_width, "height": img_height}
import csv
import json
import os
import pickle
from pathlib import Path
import cv2

category2id = {}
id2category = {}

with open('/data/pcl/proj/object-centric-ovd/tools/category_id_info.csv', encoding='utf-8-sig', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        label, value = row
        label = label.replace(' ', '_')
        value = int(value)
        category2id[label] = value
        id2category[value] = label

image_folder = Path("/data/pcl/proj/object-centric-ovd/datasets/5images/images")
img_counter = 0

img_infos = []
category_info = {}
category_info_list = []

for image_file in image_folder.glob("*"):
    # get the cat_id by reading the corresponding json file
    image_name = image_file.stem
    if image_name == 'a001':
        cat_ids = category2id['baseball_field']

    elif image_name == 'a002':
        cat_ids = category2id['basketball_court']

    elif image_name == 'a003':
        cat_ids = category2id['bridge']

    elif image_name == 'a004':
        cat_ids = category2id['chimney']

    elif image_name == 'a005':
        cat_ids = category2id['dam']

    file_name = image_file.name

    img_width = cv2.imread(str(image_file)).shape[1]
    img_height = cv2.imread(str(image_file)).shape[0]

    img_info = {"id": img_counter, "file_name": file_name, "pos_category_ids": cat_ids, "width": img_width, "height": img_height}
    img_counter += 1
    img_infos.append(img_info)

# convert the category_info to list
category_info_list = []
for cat_id, img_count in category_info.items():
    cat_info = {"id": cat_id, "name": id2category[cat_id], "image_count": img_count}
    category_info_list.append(cat_info)

with open(os.path.join('/data/pcl/proj/object-centric-ovd/datasets/5images/fake_image_info.json'), 'w') as f:
    out = {'categories': category_info_list, 'images': img_infos, 'annotations': []}
    f = json.dump(out, f)
