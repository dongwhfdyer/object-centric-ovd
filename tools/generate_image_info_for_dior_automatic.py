# img_info = {"id": img_counter, "file_name": img_path, "pos_category_ids": [category2id[folder]], "width": img_width, "height": img_height}
import csv
import json
import os
import pickle
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

image_folder = Path("datasets/DIOR_automatic_label/image_lable")
anno_folder = Path("datasets/DIOR_automatic_label/pkl")
img_counter = 0

img_infos = []
category_info ={}
category_info_list = []
# cat_info = {"id": category2id[folder], "name": category, "image_count": num_images}
def get_cat_ids_from_pkl(anno_folder, stem):
    json_path = anno_folder / (stem + '.pkl')
    with open(json_path, 'rb') as f:
        anno = pickle.load(f)
        for key in anno:
            if key not in category_info:
                category_info[key] = 1
            else:
                category_info[key] += len(anno[key][0])
    return list(anno.keys())





for image_file in image_folder.glob("*.jpg"):
    # get the cat_id by reading the corresponding json file
    cat_ids = get_cat_ids_from_pkl(anno_folder, image_file.stem)
    file_name = image_file.stem + '.jpg'

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

with open(os.path.join('datasets/DIOR_automatic_label/DIOR_automatic_image_info.json'), 'w') as f:
    out = {'categories': category_info_list, 'images': img_infos, 'annotations': []}
    f = json.dump(out, f)
