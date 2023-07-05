import pickle
from pathlib import Path

pkl_file = Path("datasets/MAVL_proposals/coco_props/class_specific/000000000009.pkl")

with open(pkl_file, "rb") as f:
    data = pickle.load(f)
    bounding_boxes = data[56][0][0]
    x_min, y_min, x_max, y_max = bounding_boxes
    print("--------------------------------------------------")


image_file = Path("datasets/coco/coco2017/train2017/000000000009.jpg")

import matplotlib.pyplot as plt

plt.imshow(plt.imread(image_file))
rect = plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, fill=False, edgecolor='green')
plt.gca().add_patch(rect)
plt.show()
print("--------------------------------------------------")

