"""
It's for MAVL.
"""
import json
import random
from pathlib import Path

import cv2

images5 = Path("/data/pcl/proj/object-centric-ovd/datasets/5images/images")

f1_edited = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_test_all_2_oriorder_ori.json")
with open(f1_edited, "r") as f:
    data1_edited = json.load(f)

# Define the category information
categories = data1_edited["categories"]

# Define the annotation information
annotations = []
image_id = 1
bbox_id = 1
images = []

for image_path in images5.iterdir():
    # ascertain the image width and height
    height, width = cv2.imread(str(image_path)).shape[:2]

    image = {
        "id": image_id,
        "width": width,
        "height": height,
        "file_name": str(image_path.name),
    }

    annotation = {
        "id": bbox_id,
        "image_id": image_id,
        "category_id": random.randint(1, 15),
        "segmentation": [],
        "area": 100,
        "bbox": [100, 100, 50, 50],
        "iscrowd": 0
    }

    annotations.append(annotation)

    bbox_id += 1

    # Increment the image ID
    image_id += 1

    images.append(image)

# Create the COCO annotation file
coco_annotation = {
    "categories": data1_edited["categories"],
    "images": images,
    "annotations": annotations
}

# Save the COCO annotation file
with open("/data/pcl/proj/object-centric-ovd/datasets/5images/fake_image_info.json", "w") as f:
    json.dump(coco_annotation, f)

# read
with open("/data/pcl/proj/object-centric-ovd/datasets/5images/fake_image_info.json", "r") as f:
    data = json.load(f)
print("--------------------------------------------------")
