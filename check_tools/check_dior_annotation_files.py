import csv
from pathlib import Path
f1 = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder.json")
dior_train_det_dataset_cat_info = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder_cat_info.json")
f1_edited = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder_2.json")
f2_edited = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder_cat_info_2.json")
f3 = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_unseen_2.json")
f4 = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2.json")
f5 = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_test_all_2.json")
DIOR_generalized_zeroshot_val= Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_test_all_2_oriorder_ori.json")
coco_orioder_cat_info =Path("datasets/coco/zero-shot/instances_train2017_seen_2_oriorder_cat_info.json")
dior_unseen_test = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_test_unseen_2.json")
coco_oriorder = Path("datasets/coco/zero-shot/instances_train2017_seen_2_oriorder.json")
import json

with open(f1, "r") as f:
    data1 = json.load(f)

# with open(f2, "r") as f:
#     data2 = json.load(f)

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

with open(DIOR_generalized_zeroshot_val, "r") as f:
    data6 = json.load(f)

with open(coco_orioder_cat_info, "r") as f:
    data7 = json.load(f)
with open(dior_unseen_test, "r") as f:
    data8 = json.load(f)

with open(coco_oriorder, "r") as f:
    data9 = json.load(f)

print("--------------------------------------------------")

