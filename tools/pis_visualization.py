# #---------kkuhn-block------------------------------ # check files
# from pathlib import Path
#
# f1 = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder.json")
# f2 = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder_cat_info.json")
# f3 = Path("datasets/coco/zero-shot/instances_train2017_seen_2_oriorder.json")
# f4 = Path("datasets/coco/zero-shot/instances_train2017_seen_2_oriorder_cat_info.json")
# f5 = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_test_all_2_oriorder.json")
# f6 = Path("datasets/remote_sensing/annotations/image_info.json")
# import json
#
# #
# with open(f1, "r") as f:
#     data1 = json.load(f)
#
# with open(f2, "r") as f:
#     data2 = json.load(f)
#
# # check coco
#
# with open(f3, "r") as f:
#     data3 = json.load(f)
#
# with open(f4, "r") as f:
#     data4 = json.load(f)
#
# with open(f5, "r") as f:
#     data5 = json.load(f)
#
# with open(f6, "r") as f:
#     data6 = json.load(f)
#
# print("--------------------------------------------------")
# #---------kkuhn-block------------------------------
import csv
import pickle
import shutil
from pathlib import Path

# with open('datasets/MAVL_proposals/rs_dior_aggregated/00001.pkl', 'rb') as f:
#     img_to_boxes = pickle.load(f)
#     proposal_box = img_to_boxes
#     print("--------------------------------------------------")


# # ---------kkuhn-block------------------------------ # visualization for dior
# dior_dataset_path = Path("datasets/DIOR/JPEGImages-trainval")
# ils_props = Path("datasets/MAVL_proposals/dior_props/classagnostic_distilfeats")
#
# import os
# import random
# import pickle
# from PIL import Image, ImageDraw
#
#
# def visualize_boxes(img_path, boxes):
#     # Open the image
#     img = Image.open(img_path)
#
#     # Draw the boxes on the image
#     draw = ImageDraw.Draw(img)
#     for box in boxes:
#         left, top, right, bottom = box
#         draw.rectangle([left, top, right, bottom], outline='red', width=2)
#
#     return img
#
#
# def main():
#     images_dir = 'datasets/DIOR/JPEGImages-trainval'
#     pkl_dir = 'datasets/MAVL_proposals/dior_props/classagnostic_distilfeats'
#     output_dir = 'rubb/visualized'
#     num_samples = 100
#
#     # delete the output directory forcefully
#     if os.path.exists(output_dir):
#         shutil.rmtree(output_dir)
#         os.makedirs(output_dir)
#
#     # Get a list of all image files
#     image_files = [f for f in os.listdir(images_dir) if f.endswith('.jpg')]
#
#     # Check if there are enough images for sampling
#     if len(image_files) < num_samples:
#         print(f"Error: The number of available images ({len(image_files)}) is less than the requested samples ({num_samples}).")
#         return
#
#     # Randomly sample image files
#     sampled_image_files = random.sample(image_files, num_samples)
#
#     for img_file in sampled_image_files:
#         img_id = img_file.split('.')[0]
#         img_path = os.path.join(images_dir, img_file)
#         pkl_path = os.path.join(pkl_dir, img_id, f'{img_id}.pkl')
#
#         # Check if the pkl file exists
#         if not os.path.exists(pkl_path):
#             print(f"Error: The pkl file for {img_file} does not exist.")
#             continue
#
#         # Load the boxes from the pkl file
#         with open(pkl_path, 'rb') as f:
#             img_to_boxes = pickle.load(f)
#
#         # Extract boxes_coordinates
#         boxes_coordinates = [item[0] for item in img_to_boxes]
#
#         # Visualize the boxes on the image
#         visualized_img = visualize_boxes(img_path, boxes_coordinates)
#
#         # Save the visualized image to the new folder
#         visualized_img.save(os.path.join(output_dir, img_file))
#
#
# if __name__ == "__main__":
#     main()
#
# # ---------kkuhn-block------------------------------

# ---------kkuhn-block------------------------------ # visualization for rs

import os
import random
import pickle
from PIL import Image, ImageDraw, ImageFont


def visualize_boxes(img_path, boxes, caption=None):
    # Open the image
    img = Image.open(img_path)

    # Draw the boxes on the image
    draw = ImageDraw.Draw(img)
    for box in boxes:
        left, top, right, bottom = box
        draw.rectangle([left, top, right, bottom], outline='red', width=2)

    # Add the caption to the upper left of the image
    if caption:
        font = ImageFont.load_default()
        text_size = draw.textsize(caption, font)
        draw.rectangle([0, 0, text_size[0], text_size[1]], fill='red')
        draw.text((0, 0), caption, fill='white', font=font)

    return img


def main():
    images_dir = 'datasets/remote_sensing/RS_images'
    pkl_dir = 'datasets/MAVL_proposals/rs_props/classagnostic_distilfeats'
    output_dir = 'rubb/visualized'

    category2id = {}
    id2category = {}

    # Open the CSV file (replace with the path to your file)
    with open('tools/category_id_info.csv', encoding='utf-8-sig', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            # remove the useless token
            label, value = row
            label = label.replace(' ', '_')
            value = int(value)
            category2id[label] = value
            id2category[value] = label

    num_samples = 100

    # delete the output directory forcefully
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)

    image_files = []

    # Walk through the directory tree and get a list of all image files
    for dirpath, dirnames, filenames in os.walk(images_dir):
        for filename in filenames:
            if filename.endswith('.jpg'):
                image_path = os.path.join(dirpath, filename)
                image_files.append(image_path)

    # Check if there are enough images for sampling
    if len(image_files) < num_samples:
        print(f"Error: The number of available images ({len(image_files)}) is less than the requested samples ({num_samples}).")
        return

    # Randomly sample image files
    sampled_image_files = random.sample(image_files, num_samples)

    for img_file in sampled_image_files:
        cat_id = img_file.split('/')[-1].split('_')[0]
        cat_name = id2category[int(cat_id)]
        img_id = img_file.split('/')[-1].split('.')[0]
        img_path = img_file
        img_file = img_file.split('/')[-1]
        pkl_path = os.path.join(pkl_dir, str(cat_id), f'{img_id}.pkl')

        # Check if the pkl file exists
        if not os.path.exists(pkl_path):
            print(f"Error: The pkl file for {img_file} does not exist.")
            continue

        # Load the boxes from the pkl file
        with open(pkl_path, 'rb') as f:
            img_to_boxes = pickle.load(f)

        # Extract boxes_coordinates
        boxes_coordinates = [item[0] for item in img_to_boxes]

        # Visualize the boxes on the image
        visualized_img = visualize_boxes(img_path, boxes_coordinates, caption=cat_name)

        # Save the visualized image to the new folder
        visualized_img.save(os.path.join(output_dir, img_file))


if __name__ == "__main__":
    main()

# ---------kkuhn-block------------------------------
