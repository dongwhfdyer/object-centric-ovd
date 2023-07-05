import pickle
import shutil
from pathlib import Path

# #---------kkuhn-block------------------------------ # dior_automatic_label
# pkl_folder = Path("datasets/DIOR_automatic_label/pkl")
# pkl_folder_2 = Path("datasets/DIOR_automatic_label/pkl2")
# #---------kkuhn-block------------------------------

#---------kkuhn-block------------------------------ # 20_merge
pkl_folder = Path("datasets/DIOR_20_Merge_labled/pkl")
pkl_folder_2 = Path("datasets/DIOR_20_Merge_labled/pkl2")
#---------kkuhn-block------------------------------
if pkl_folder_2.exists():
    shutil.rmtree(pkl_folder_2)
pkl_folder_2.mkdir()

for pkl_file in pkl_folder.glob("*.pkl"):
    with open(pkl_file, "rb") as f:
        data = pickle.load(f)
        new_data = {}
        for key in data.keys():
            bounding_boxes = data[key][0]
            new_bounding_boxes = []
            for bounding_box in bounding_boxes:
                # convert xyxy to x_min, y_min, width, height
                x_min = bounding_box[0]
                y_min = bounding_box[1]
                width = bounding_box[2] - x_min
                height = bounding_box[3] - y_min
                new_bounding_boxes.append([x_min, y_min, width, height])

            new_data[key] = (new_bounding_boxes, data[key][1])

    with open(pkl_folder_2 / pkl_file.name, "wb") as f:
        pickle.dump(new_data, f)

        print("--------------------------------------------------")


