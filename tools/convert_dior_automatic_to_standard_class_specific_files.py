import json
import pickle
import shutil
from pathlib import Path

original_json_folder = Path("datasets/DIOR_automatic_label/json")
output_pkl_folder = Path("datasets/DIOR_automatic_label/pkl")

# delete the output folder if it exists
if output_pkl_folder.exists():
    shutil.rmtree(output_pkl_folder)

# create the output folder
output_pkl_folder.mkdir(parents=True)


for json_file in original_json_folder.glob("*.json"):
    with open(json_file, "r") as f:
        data = json.load(f)
        pkl_dict = {}
        for i in range(len(data['mask'])):
            if 'class' not in data['mask'][i]:
                continue
            category_id = data['mask'][i]['class']
            if category_id not in pkl_dict:
                bounding_box = data['mask'][i]['box']
                pkl_dict[category_id] = ([bounding_box],[0.98])
            else:
                bounding_box = data['mask'][i]['box']
                pkl_dict[category_id][0].append(bounding_box)
                pkl_dict[category_id][1].append(0.98)
            print("--------------------------------------------------")

    pkl_file = output_pkl_folder / (json_file.stem + ".pkl")

    with open(pkl_file, "wb") as f:
        pickle.dump(pkl_dict, f)

