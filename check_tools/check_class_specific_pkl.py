import pickle
from pathlib import Path

file_path = "datasets/DIOR_20_Merge_labled/pkl/0_airplane,aircraft,aeroplane_1.pkl"

with open(file_path, "rb") as f:
    data = pickle.load(f)
    print("--------------------------------------------------")

bounding_boxes = data[0][0][0]
x_min, y_min, x_max, y_max = bounding_boxes

image_file = Path("datasets/CLASS_20_merge/0_airplane,aircraft,aeroplane_1.jpg")

import matplotlib.pyplot as plt

plt.imshow(plt.imread(image_file))
rect = plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, fill=False, edgecolor='green')
plt.gca().add_patch(rect)
plt.show()
print("--------------------------------------------------")

