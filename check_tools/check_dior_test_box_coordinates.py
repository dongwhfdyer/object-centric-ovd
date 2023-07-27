from pathlib import Path
import shutil

from matplotlib import pyplot as plt
from tqdm import tqdm

#---------kkuhn-block------------------------------ # for test
test_json = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_test_all_2_oriorder_ori.json")
image_folder = Path("datasets/DIOR/JPEGImages-test")
output_folder = Path("rubb/dior_test_visualized")
#---------kkuhn-block------------------------------

# #---------kkuhn-block------------------------------ # for train
# test_json = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_test_all_2_oriorder_ori.json")
# image_folder = Path("datasets/DIOR/JPEGImages-test")
# output_folder = Path("rubb/dior_test_visualized")
# #---------kkuhn-block------------------------------
if output_folder.exists():
    shutil.rmtree(output_folder)
output_folder.mkdir(parents=True, exist_ok=True)


import json

with open(test_json, "r") as f:
    data = json.load(f)
    anno = data["annotations"]

tbar = tqdm( total=len(list(image_folder.glob("*.jpg"))))


for img in image_folder.glob("*.jpg"):
    tbar.update(1)
    # print(img.stem)
    plt.imshow(plt.imread(img))
    for a in anno:
        if a["image_id"] == img.stem:
            x1, y1, width, height = a['bbox']
            rect = plt.Rectangle((x1, y1), width, height, fill=False, edgecolor='green')
            plt.gca().add_patch(rect)
            plt.text(x1, y1 - 5, f"Class {a['category_id']}", color='green')

    # plt.show()
    plt.savefig(str(output_folder / img.name))
    plt.close()








