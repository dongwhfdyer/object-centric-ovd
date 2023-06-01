"""
After changing the original `image_info.json`, we need to change the `rs_pis_aggregated.json` manually.
"""

import json

ref_json_path = f"datasets/remote_sensing/annotations/image_info.json"
json_to_be_edited = f"datasets/remote_sensing/annotations/rs_pis_aggregated.json"

with open(ref_json_path, "r") as f:
    ref_json_contents = json.load(f)
# Dict to save in target json file
categories = ref_json_contents['categories']

with open(json_to_be_edited, "r") as f:
    json_to_be_edited_contents = json.load(f)

# change the json_to_be_edited's categories to ref_json's categories
json_to_be_edited_contents['categories'] = categories

with open(json_to_be_edited, "w") as f:
    json.dump(json_to_be_edited_contents, f)
