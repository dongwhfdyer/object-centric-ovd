import csv
import json
import pickle
import shutil
import warnings
from pathlib import Path

import cv2

train_json = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder.json")
val_json = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_test_all_2_oriorder_ori.json")

train_image_folder = Path("datasets/DIOR/JPEGImages-trainval")
val_image_folder = Path("datasets/DIOR/JPEGImages-test")

pkl_folder = Path("datasets/DIOR/Annotations/pkl")
image_info_json = Path("datasets/DIOR/Annotations/image_info_real_psuedo_proposals.json")

if pkl_folder.exists():
    shutil.rmtree(pkl_folder, ignore_errors=True)
pkl_folder.mkdir(parents=True)

# ---------kkuhn-block------------------------------ # read category_id_info.csv
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
# ---------kkuhn-block------------------------------


images_dict = {}
category_dict = {}
# ---------kkuhn-block------------------------------ # tackle train set
with open(train_json, "r") as f:
    data = json.load(f)

for annotation in data['annotations']:
    image_id = annotation['image_id']
    category_id = annotation['category_id']
    category_dict[category_id] = category_dict.get(category_id, 0) + 1
    bbox = annotation['bbox']
    if image_id not in images_dict:
        images_dict[image_id] = {}
        images_dict[image_id][category_id] = ([bbox], [0.98])

    else:
        if category_id not in images_dict[image_id]:
            images_dict[image_id][category_id] = ([bbox], [0.98])
        else:
            images_dict[image_id][category_id][0].append(bbox)
            images_dict[image_id][category_id][1].append(0.98)
# ---------kkuhn-block------------------------------

# ---------kkuhn-block------------------------------ # tackle val set
with open(val_json, "r") as f:
    val_data = json.load(f)

for annotation in val_data['annotations']:
    image_id = annotation['image_id']
    category_id = annotation['category_id']
    category_dict[category_id] = category_dict.get(category_id, 0) + 1
    bbox = annotation['bbox']
    if image_id not in images_dict:
        images_dict[image_id] = {}
        images_dict[image_id][category_id] = ([bbox], [0.98])

    else:
        if category_id not in images_dict[image_id]:
            images_dict[image_id][category_id] = ([bbox], [0.98])
        else:
            images_dict[image_id][category_id][0].append(bbox)
            images_dict[image_id][category_id][1].append(0.98)


# ---------kkuhn-block------------------------------

def get_width_height(image_id):
    # locate image: whether it's under the train_image_folder or val_image_folder
    if (train_image_folder / (image_id + '.jpg')).exists():


        image = cv2.imread(str(train_image_folder / (image_id + '.jpg')))
        height, width, _ = image.shape
    elif (val_image_folder / (image_id + '.jpg')).exists():
        image = cv2.imread(str(val_image_folder / (image_id + '.jpg')))
        height, width, _ = image.shape
    else:
        raise Exception("image not found")



    # #---------kkuhn-block------------------------------ # use try-catch
    #
    # try:
    #     image = cv2.imread(str(train_image_folder / (image_id + '.jpg')))
    #     height, width, _ = image.shape
    # except Exception as e:
    #     image = cv2.imread(str(val_image_folder / (image_id + '.jpg')))
    #     height, width, _ = image.shape
    # except Exception as e:
    #     print("not work for image_id: ", image_id)
    #     raise e
    #
    # #---------kkuhn-block------------------------------

    return width, height

img_infos = []
img_counter = 0
for image_dict in images_dict:
    pkl_file = pkl_folder / (str(image_dict) + ".pkl")
    width, height = get_width_height(image_dict)
    img_info = {"id": img_counter, "file_name": str(image_dict) + ".jpg", "pos_category_ids": list(images_dict[image_dict].keys()), "width": width, "height": height}
    with open(pkl_file, "wb") as f:
        pickle.dump(images_dict[image_dict], f)

    img_counter += 1
    img_infos.append(img_info)

category_info_list = []
for cat_id, img_count in category_dict.items():
    cat_info = {"id": cat_id, "name": id2category[cat_id], "image_count": img_count}
    category_info_list.append(cat_info)

with open(image_info_json, 'w') as f:
    out = {'categories': category_info_list, 'images': img_infos, 'annotations': []}
    f = json.dump(out, f)

# read back
with open(image_info_json, 'r') as f:
    data = json.load(f)
    print("--------------------------------------------------")
