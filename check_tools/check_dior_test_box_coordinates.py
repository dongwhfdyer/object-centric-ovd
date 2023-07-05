from pathlib import Path

from matplotlib import pyplot as plt

test_json = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_test_all_2_oriorder_ori.json")
image_folder = Path("datasets/DIOR/JPEGImages-test")

import json

with open(test_json, "r") as f:
    data = json.load(f)
    anno = data["annotations"]

for img in image_folder.glob("*.jpg"):
    print(img.stem)
    plt.imshow(plt.imread(img))
    for a in anno:
        if a["image_id"] == img.stem:
            x1, y1, width, height = a['bbox']
            rect = plt.Rectangle((x1, y1), width, height, fill=False, edgecolor='green')
            plt.gca().add_patch(rect)
            plt.text(x1, y1 - 5, f"Class {a['category_id']}", color='green')
    plt.show()
    print("--------------------------------------------------")






