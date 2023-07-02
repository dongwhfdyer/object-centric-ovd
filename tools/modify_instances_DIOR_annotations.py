import json
from pathlib import Path

f5 = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_test_all_2.json")
f5_int_id = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_test_all_2_int_id.json")

f4 = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2.json")
f4_int_id = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_int_id.json")

with open(f5, "r") as f:
    data5 = json.load(f)
    images = data5["images"]
    for image in images:
        image["id"] = int(image["id"])
    annotaions = data5["annotations"]
    for annotaion in annotaions:
        annotaion["image_id"] = int(annotaion["image_id"])


    data5["images"] = images
    data5["annotations"] = annotaions

with open(f5_int_id, "w") as f:
    json.dump(data5, f)

with open(f4, "r") as f:
    data4 = json.load(f)
    images = data4["images"]
    for image in images:
        image["id"] = int(image["id"])
    annotaions = data4["annotations"]
    for annotaion in annotaions:
        annotaion["image_id"] = int(annotaion["image_id"])

    data4["images"] = images
    data4["annotations"] = annotaions

with open(f4_int_id, "w") as f:
    json.dump(data4, f)

print("--------------------------------------------------")
