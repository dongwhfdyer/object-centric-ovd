"""
This script creates a single json file to be used for ILS from the image-level pkl files. This is not mandatory,
however, doing so improves training efficiency. Don't set 'PIS_PROP_PATH' path in config if using single json file.\

Examples:
    python tools/create_lvis_ils_json.py -dataset_dir datasets/imagenet
    -prop_path datasets/MAVL_proposals/lvis_props/class_specific/imagenet_lvis_props
    -target_path datasets/imagenet/annotations/imagenet_lvis_image_info_pis.json
"""

import argparse
import json
from tqdm import tqdm
import os
import pickle


def parse_arguments():
    """
    Parse the command line arguments
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-dataset_dir", "--dataset_base_dir_path", required=False, default='datasets/imagenet',
                    help="The dataset base directory path.")
    ap.add_argument("-prop_path", "--mavl_proposal_path", required=False,
                    default='datasets/MAVL_proposals/lvis_props/class_specific/imagenet_lvis_props',
                    help="Path to the generated MAVL proposals (one pkl file for one image)")
    ap.add_argument("-target_path", "--target_file_path", required=False,
                    default='datasets/imagenet/annotations/imagenet_lvis_image_info_pis.json',
                    help="Path to save the generated json file.")

    args = vars(ap.parse_args())

    return args


def main():
    # Parse arguments
    args = parse_arguments()
    dataset_dir = args["dataset_base_dir_path"]
    mavl_prop_path = args["mavl_proposal_path"]
    target_json_path = args["target_file_path"]
    # Reference json file
    if "remote_sensing" in dataset_dir:
        ref_json_path = f"{dataset_dir}/annotations/image_info.json"
    else:
        ref_json_path = f"{dataset_dir}/annotations/imagenet_lvis_image_info.json"
    print("Reference json path: ", ref_json_path)
    # Read the reference json
    with open(ref_json_path) as f:
        ref_json_contents = json.load(f)
    # Dict to save in target json file
    categories = ref_json_contents['categories']
    annotations = []
    images = []
    ann_id = 1
    for image in tqdm(ref_json_contents['images']):
        file_name = image['file_name']
        image_id = image['id']
        category_id = str(image['pos_category_ids'][0])
        image_name = os.path.basename(file_name)
        image_name = image_name.split('.')[0]
        img_path = f"{mavl_prop_path}/{category_id}/{image_name}.pkl"
        if os.path.exists(img_path):
            # Read pkl file and load box and category
            with open(img_path, "rb") as f:
                detections = pickle.load(f)
            target_keys = detections.keys()
            for k in target_keys:
                # for each target apply transforms
                box, prob = detections[k]
                box, prob = box[0], prob[0]  # Assuming there is only one box
                box_area = (box[3] - box[1]) * (box[2] - box[0])
                # switch box to normal list and as int values
                box = box.astype(int).tolist()
                box_area = int(box_area)
                annotation = {'area': box_area, 'id': ann_id, 'image_id': image_id, 'bbox': box, 'category_id': k}
                annotations.append(annotation)
                ann_id += 1
            images.append(image)
    # Save the json
    print(f"Writing json...")
    out_data = {'images': images, 'categories': categories, 'annotations': annotations}
    json.dump(out_data, open(target_json_path, 'w'))


if __name__ == "__main__":
    main()
    # python tools/create_lvis_ils_json.py -dataset_dir datasets/remote_sensing -prop_path datasets/MAVL_proposals/rs_props/class_specific -target_path datasets/remote_sensing/annotations/rs_pis_aggregated.json
    # python tools/create_lvis_ils_json.py -dataset_dir datasets/remote_sensing -prop_path datasets/MAVL_proposals/rs_20_props/class_specific -target_path datasets/remote_sensing/annotations/rs_20_pis_aggregated.json
    # python tools/create_lvis_ils_json.py -dataset_dir datasets/rs_20_merge -prop_path datasets/DIOR_20_Merge_labled/pkl -target_path datasets/DIOR_20_Merge_labled/rs_20_merge_pis_aggregated.json
