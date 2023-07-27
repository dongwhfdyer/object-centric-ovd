import json
import pickle
from pathlib import Path

import cv2

image_folder = Path("datasets/DIOR_automatic_label/orig_images")
anno_folder = Path("datasets/DIOR_automatic_label/pkl")

one_other_image = Path("datasets/DIOR_automatic_label/orig_images/00011.jpg")
one_s_pkl = Path("datasets/DIOR_automatic_label/pkl/00011.pkl")

# cls_anno_json = Path("datasets/DIOR_automatic_label/DIOR_automatic_image_info.json")
# with open(cls_anno_json, "r") as f:
#     data = json.load(f)

# select 100 "bridge"
num = 0

bridge_images = []

# #---------kkuhn-block------------------------------ # deprecated
# for img_content in data["images"]:
#     if 4 in img_content["pos_category_ids"]:
#         file_name = img_content["file_name"]
#         bridge_images.append(file_name)
#         num += 1
# # ---------kkuhn-block------------------------------

for pkl_path in anno_folder.glob("*.pkl"):
    with open(pkl_path, 'rb') as f:
        anno = pickle.load(f)
        if 4 in anno:
            bridge_images.append(pkl_path.stem + '.jpg')
            num += 1
            if num == 100:
                break



for bridge_image in bridge_images:
    img_path = image_folder / bridge_image
    pkl_path = anno_folder / (bridge_image[:-4] + '.pkl')

    with open(pkl_path, 'rb') as f:
        anno = pickle.load(f)
        bounding_box = anno[4][0][0]

        print("--------------------------------------------------")
        break
        # boundingbox



# # cls: read image, boundingbox, and label
# cls_image =cv2.imread(str(cls_image_path))
#
#
# # det: read image, boundingbox, and label
# det_image =cv2.imread(str(det_image_path))
