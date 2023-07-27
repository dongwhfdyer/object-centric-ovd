import json
import pickle
import shutil
from pathlib import Path

original_json_folder = Path("datasets/DIOR_20_Merge_labled/json")
output_pkl_folder = Path("datasets/DIOR_20_Merge_labled/pkl")

# delete the output folder if it exists
if output_pkl_folder.exists():
    shutil.rmtree(output_pkl_folder)

# create the output folder
output_pkl_folder.mkdir(parents=True)

for json_file in original_json_folder.glob("*.json"):
    with open(json_file, "r") as f:
        data = json.load(f)
        pkl_dict = {}
        category_id = int(data['image_name'].split('_')[0])
        bounding_boxes = []
        confidence = []
        for bounding_box_item in data['mask'][1:]:
            bounding_boxes.append(bounding_box_item['box'])
            confidence.append(0.98)

        pkl_dict[category_id] = (bounding_boxes, [0.98])
        print("--------------------------------------------------")

    pkl_file = output_pkl_folder / (json_file.stem + ".pkl")

    with open(pkl_file, "wb") as f:
        pickle.dump(pkl_dict, f)
