import csv
from pathlib import Path

f1 = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder.json")
f2 = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder_cat_info.json")
f1_edited = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder_2.json")
f2_edited = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder_cat_info_2.json")
f3 = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_unseen_2.json")
f4 = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2.json")
f5 = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_test_all_2.json")

import json

with open(f1, "r") as f:
    data1 = json.load(f)

with open(f2, "r") as f:
    data2 = json.load(f)

with open(f1_edited, "r") as f:
    data1_edited = json.load(f)

with open(f2_edited, "r") as f:
    data2_edited = json.load(f)


with open(f3, "r") as f:
    data3 = json.load(f)

with open(f4, "r") as f:
    data4 = json.load(f)

with open(f5, "r") as f:
    data5 = json.load(f)

print("--------------------------------------------------")

