"""
This script uses MAVL from paper https://arxiv.org/abs/2111.11430 to generate class-specific boxes for Image-level
supervision in our approach. Specifically, we use "every <category name>" and selects top-1 proposal for each category
present in an image.

Examples:
    - Clone the external modules:
        git submodule init
        git submodule update
    - Set the PYTHONPATH:
        export PYTHONPATH="./external/mavl:$PYTHONPATH"
    - Run
    For COCO:
        python tools/get_ils_labels.py -ckpt <mavl pretrained weights path> -dataset coco -dataset_dir datasets/coco
        -output datasets/MAVL_proposals/coco_props/class_specific
    For ImageNet-LVIS
        python tools/get_ils_labels.py -ckpt <mavl pretrained weights path> -dataset imagenet_lvis
        -dataset_dir datasets/imagenet -output datasets/MAVL_proposals/lvis_props/class_specific/imagenet_lvis_props
"""
import asyncio
import shutil
import sys

import os

# sys.path.append('/data/pcl/proj/object-centric-ovd/external')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import argparse
import json
from tqdm import tqdm
import numpy as np

from external.mavl.models.model import Model
from utils.save_proposal_boxes import SaveProposalBoxes

from utils.get_coco_ils_query import get_query as get_coco_query
from utils.get_lvis_ils_query import get_query as get_lvis_query
from utils.get_rs_ils_query import get_query as get_rs_query


def parse_arguments():
    """
    Parse the command line arguments
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-ckpt", "--mavl_checkpoints_path", required=True,
                    help="The path to MAVL pretrained weights.")
    ap.add_argument("-dataset", "--dataset_name", required=False, default='coco',
                    help="The dataset name to generate the ILS labels for. Supported datasets are "
                         "['coco', 'imagenet_lvis']")
    ap.add_argument("-dataset_dir", "--dataset_base_dir_path", required=False, default='datasets/coco',
                    help="The dataset base directory path.")
    ap.add_argument("-output", "--output_dir_path", required=False,
                    default='datasets/MAVL_proposals/coco_props/class_specific',
                    help="Path to save the ILS labels.")

    args = vars(ap.parse_args())

    return args


def parse_coco_annotations(filename):
    dataset = json.load(open(filename, 'r'))
    assert type(dataset) == dict, 'annotation file format {} not supported'.format(type(dataset))
    annos = {}
    all_annos = dataset["images"]
    for ann in all_annos:
        imag_name = ann["file_name"].split('.')[0]
        categories = ann["pos_category_ids"]
        annos[imag_name] = categories

    return annos


def get_top_1_mavl_box(image_path, text_query, confidence):
    boxes, scores = model.infer_image(image_path, caption=text_query)
    # Select top-1 box
    scores = np.array(scores)
    boxes = np.array(boxes)
    max_score_index = np.argmax(scores)
    box, score = [], []
    # Consider only if score > conf_thresh
    if scores[max_score_index] > confidence:
        box.append(boxes[max_score_index])
        score.append(scores[max_score_index])

    return box, score


def get_top_n_mavl_boxes(image_path, text_query, confidence, n=5):
    boxes, scores = model.infer_image(image_path, caption=text_query)

    scores = np.array(scores)
    boxes = np.array(boxes)

    sorted_indices = np.argsort(scores)[::-1][:n]

    top_boxes = []
    top_scores = []

    for i in sorted_indices:
        if scores[i] > confidence:
            top_boxes.append(boxes[i])
            top_scores.append(scores[i])

    return top_boxes, top_scores


def get_coco_ils_labels(dataset_dir, save_dir, conf_thresh=0.95):
    train_images_path = f"{dataset_dir}/train2017"
    ils_annotation_path = f"{dataset_dir}/annotations/captions_train2017_tags_allcaps.json"
    # The coco dataset must be setup correctly before running this script, see datasets/README.md for details
    assert os.path.exists(train_images_path)
    assert os.path.exists(ils_annotation_path)

    annotations = parse_coco_annotations(ils_annotation_path)  # Parse annotations to get image-level labels
    dumper = SaveProposalBoxes()  # Create dumper to save generated boxes (labels) in pkl format
    # Iterate over all the images and generate ILS labels
    detections = {}
    missing = 0
    for i, image_name in enumerate(tqdm(os.listdir(train_images_path))):
        if i > 0 and i % 500 == 0:  # Save every 500 iterations
            dumper.update(detections)
            dumper.save(save_dir)
            detections = {}
        image_path = f"{train_images_path}/{image_name}"
        image_name_key = image_name.split('.')[0]
        if image_name_key in annotations:
            annotation = annotations[image_name.split('.')[0]]
        else:
            annotation = None
            missing += 1
        preds = {}
        if annotation is not None:
            for target in annotation:
                query, _ = get_coco_query(target)
                preds[target] = get_top_1_mavl_box(image_path, query, conf_thresh)
        detections[image_name_key] = preds
    dumper.update(detections)
    dumper.save(save_dir)
    print("Total number of images not present in caption dataset is,", missing)


def get_imagenet_lvis_ils_labels(dataset_dir, save_dir, conf_thresh=0.0):
    images_path = f"{dataset_dir}/ImageNet-LVIS"
    ils_annotation_path = f"{dataset_dir}/annotations/imagenet_lvis_image_info.json"
    # The coco dataset must be setup correctly before running this script, see datasets/README.md for details
    assert os.path.exists(images_path)
    assert os.path.exists(ils_annotation_path)

    annotations = parse_coco_annotations(ils_annotation_path)  # Parse annotations to get image-level labels
    dumper = SaveProposalBoxes()  # Create dumper to save generated boxes (labels) in pkl format
    # Iterate over all the images and generate ILS labels
    detections = {}
    missing = 0
    images = annotations.keys()
    for i, image_name_key in enumerate(tqdm(images)):
        if i > 0 and i % 5 == 0:  # Save every 500 iterations
            dumper.update(detections)
            dumper.save_imagenet(save_dir)

            detections = {}
        image_path = f"{images_path}/{image_name_key}.JPEG"
        image_name = os.path.basename(image_name_key)
        if image_name_key in annotations:
            annotation = annotations[image_name_key]
        else:
            annotation = None
            missing += 1
        preds = {}
        if annotation is not None:
            for target in annotation:
                query, _ = get_lvis_query(target)
                preds[target] = get_top_1_mavl_box(image_path, query, conf_thresh)
        detections[image_name] = preds
    dumper.update(detections)
    dumper.save_imagenet(save_dir)
    print("Total number of images not present in caption dataset is,", missing)


def get_rs_ils_labels(dataset_dir, save_dir, conf_thresh=0.0):
    images_path = f"{dataset_dir}/RS_images"
    ils_annotation_path = f"{dataset_dir}/annotations/image_info.json"
    # The coco dataset must be setup correctly before running this script, see datasets/README.md for details
    assert os.path.exists(images_path)
    assert os.path.exists(ils_annotation_path)

    # ---------kkuhn-block------------------------------ # empty the save_dir
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
    # ---------kkuhn-block------------------------------

    annotations = parse_coco_annotations(ils_annotation_path)  # Parse annotations to get image-level labels
    dumper = SaveProposalBoxes()  # Create dumper to save generated boxes (labels) in pkl format
    # Iterate over all the images and generate ILS labels
    detections = {}
    missing = 0
    images = annotations.keys()
    for i, image_name_key in enumerate(tqdm(images)):
        if i > 0 and i % 5 == 0:  # Save every 500 iterations
            dumper.update(detections)
            dumper.save_imagenet(save_dir)

            detections = {}
        image_path = f"{images_path}/{image_name_key}.jpg"
        image_name = os.path.basename(image_name_key)
        if image_name_key in annotations:
            annotation = annotations[image_name_key]
        else:
            annotation = None
            missing += 1
        preds = {}
        if annotation is not None:
            for target in annotation:
                query, _ = get_rs_query(target)
                preds[target] = get_top_1_mavl_box(image_path, query, conf_thresh)
        detections[image_name] = preds
    dumper.update(detections)
    dumper.save_imagenet(save_dir)
    print("Total number of images not present in caption dataset is,", missing)


def get_rs_20_ils_labels(dataset_dir, save_dir, conf_thresh=0.0):
    images_path = f"{dataset_dir}/RS_images_20"
    ils_annotation_path = f"{dataset_dir}/annotations/rs_20_image_info.json"
    # The coco dataset must be setup correctly before running this script, see datasets/README.md for details
    assert os.path.exists(images_path)
    assert os.path.exists(ils_annotation_path)

    # ---------kkuhn-block------------------------------ # empty the save_dir
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
    # ---------kkuhn-block------------------------------

    annotations = parse_coco_annotations(ils_annotation_path)  # Parse annotations to get image-level labels
    dumper = SaveProposalBoxes()  # Create dumper to save generated boxes (labels) in pkl format
    # Iterate over all the images and generate ILS labels
    detections = {}
    missing = 0
    images = annotations.keys()
    for i, image_name_key in enumerate(tqdm(images)):
        if i > 0 and i % 5 == 0:  # Save every 500 iterations
            dumper.update(detections)
            dumper.save_imagenet(save_dir)

            detections = {}
        image_path = f"{images_path}/{image_name_key}.jpg"
        image_name = os.path.basename(image_name_key)
        if image_name_key in annotations:
            annotation = annotations[image_name_key]
        else:
            annotation = None
            missing += 1
        preds = {}
        if annotation is not None:
            for target in annotation:
                query, _ = get_rs_query(target)
                preds[target] = get_top_1_mavl_box(image_path, query, conf_thresh)
        detections[image_name] = preds
    dumper.update(detections)
    dumper.save_imagenet(save_dir)
    print("Total number of images not present in caption dataset is,", missing)


def get_merge_split_1_ils_labels(dataset_dir, save_dir, conf_thresh=0.0):
    images_path = f"{dataset_dir}"
    ils_annotation_path = f"datasets/dior_5_split_1_unseen_lable/DIOR_5_split_1_unseen_image_info.json"
    # The coco dataset must be setup correctly before running this script, see datasets/README.md for details
    assert os.path.exists(images_path)
    assert os.path.exists(ils_annotation_path)

    # ---------kkuhn-block------------------------------ # empty the save_dir
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
    # ---------kkuhn-block------------------------------

    annotations = parse_coco_annotations(ils_annotation_path)  # Parse annotations to get image-level labels
    dumper = SaveProposalBoxes()  # Create dumper to save generated boxes (labels) in pkl format
    # Iterate over all the images and generate ILS labels
    detections = {}
    missing = 0
    images = annotations.keys()
    for i, image_name_key in enumerate(tqdm(images)):
        if i > 0 and i % 5 == 0:  # Save every 500 iterations
            dumper.update(detections)
            dumper.save_imagenet(save_dir)

            detections = {}
        image_path = f"{images_path}/{image_name_key}.jpg"
        image_name = os.path.basename(image_name_key)
        if image_name_key in annotations:
            annotation = annotations[image_name_key]
        else:
            annotation = None
            missing += 1
        preds = {}
        if annotation is not None:
            for target in annotation:
                query, _ = get_rs_query(target)
                preds[target] = get_top_1_mavl_box(image_path, query, conf_thresh)
        detections[image_name] = preds
    dumper.update(detections)
    dumper.save_imagenet(save_dir)
    print("Total number of images not present in caption dataset is,", missing)


def get_5_images_ils_labels(dataset_dir, save_dir, conf_thresh=0.0):
    images_path = f"{dataset_dir}"
    ils_annotation_path = f"datasets/5images/fake_image_info.json"

    assert os.path.exists(images_path)
    assert os.path.exists(ils_annotation_path)

    # ---------kkuhn-block------------------------------ # empty the save_dir
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
    # ---------kkuhn-block------------------------------

    annotations = parse_coco_annotations(ils_annotation_path)  # Parse annotations to get image-level labels
    dumper = SaveProposalBoxes()  # Create dumper to save generated boxes (labels) in pkl format
    # Iterate over all the images and generate ILS labels
    detections = {}
    missing = 0
    images = annotations.keys()
    for i, image_name_key in enumerate(tqdm(images)):
        if i > 0 and i % 5 == 0:  # Save every 500 iterations
            dumper.update(detections)
            dumper.save_imagenet(save_dir)

            detections = {}
        image_path = f"{images_path}/{image_name_key}.jpg"
        if image_name_key == 'a004':
            image_path = f"{images_path}/{image_name_key}.png"
        image_name = os.path.basename(image_name_key)
        target = annotations[image_name_key]
        preds = {}
        query, _ = get_rs_query(target)
        preds[target] = get_top_n_mavl_boxes(image_path, query, conf_thresh, 30)
        detections[image_name] = preds
    dumper.update(detections)
    dumper.save_imagenet(save_dir)
    print("Total number of images not present in caption dataset is,", missing)


if __name__ == "__main__":
    # Parse the arguments
    args = parse_arguments()
    mavl_checkpoints_path = args["mavl_checkpoints_path"]
    dataset_name = args["dataset_name"]
    dataset_base_dir = args["dataset_base_dir_path"]
    output_dir = args["output_dir_path"]
    os.makedirs(output_dir, exist_ok=True)

    # Load MAVL model
    model = Model("mdef_detr", mavl_checkpoints_path).get_model()
    # Generate ILS labels
    if dataset_name == "coco":
        get_coco_ils_labels(dataset_base_dir, output_dir)
    elif dataset_name == "imagenet_lvis":
        # asyncio.run(get_imagenet_lvis_ils_labels(dataset_base_dir, output_dir))
        get_imagenet_lvis_ils_labels(dataset_base_dir, output_dir)
    elif dataset_name == "rs":
        get_rs_ils_labels(dataset_base_dir, output_dir)
    elif dataset_name == "rs_20":
        get_rs_20_ils_labels(dataset_base_dir, output_dir)
    elif dataset_name == "merge_split_1":
        get_merge_split_1_ils_labels(dataset_base_dir, output_dir)
    elif dataset_name == "5_images":
        get_5_images_ils_labels(dataset_base_dir, output_dir)
    else:
        print(f"Only 'coco' and 'imagenet_lvis' datasets are supported.")
        raise NotImplementedError
# python tools/get_ils_labels.py -ckpt saved_models/MDef_DETR_r101_epoch20.pth -dataset imagenet_lvis -dataset_dir datasets/imagenet -output datasets/MAVL_proposals/lvis_props/class_specific/imagenet_lvis_props
# python tools/get_ils_labels.py -ckpt saved_models/MDef_DETR_r101_epoch20.pth -dataset rs -dataset_dir datasets/remote_sensing -output datasets/MAVL_proposals/rs_props/class_specific/
# python tools/get_ils_labels.py -ckpt saved_models/MDef_DETR_r101_epoch20.pth -dataset rs_20 -dataset_dir datasets/remote_sensing -output datasets/MAVL_proposals/rs_20_props/class_specific/
# python tools/get_ils_labels.py -ckpt saved_models/MDef_DETR_r101_epoch20.pth -dataset merge_split_1 -dataset_dir datasets/merge_split_1 -output datasets/MAVL_proposals/merge_split_1_props/class_specific/
# python tools/get_ils_labels.py -ckpt saved_models/MDef_DETR_r101_epoch20.pth -dataset 5_images -dataset_dir datasets/5images/images -output datasets/MAVL_proposals/5images/class_specific/
