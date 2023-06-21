import csv
from pathlib import Path

f1 = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder.json")
f2 = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder_cat_info.json")
f1_edited = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder_2.json")
f2_edited = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder_cat_info_2.json")

import json

with open(f1, "r") as f:
    data1 = json.load(f)

with open(f2, "r") as f:
    data2 = json.load(f)

category2id = {}
id2category = {}
extend_categories_1 = []
extend_categories_2 = []
with open('tools/category_id_info.csv', encoding='utf-8-sig', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        # skip the first 20 rows
        if reader.line_num <= 20:
            continue
        label, value = row
        value = int(value)
        category2id[label] = value
        id2category[value] = label
        extend_categories_1.append(
            {'id': value, 'name': label}
        )
        extend_categories_2.append(
            {'id': value, 'image_count': 0, 'instance_count': 0, 'name': label}
        )

data1['categories'].extend(extend_categories_1)
data2.extend(extend_categories_2)

with open(f1_edited, "w") as f:
    json.dump(data1, f)

with open(f2_edited, "w") as f:
    json.dump(data2, f)
