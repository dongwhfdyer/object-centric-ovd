import shutil

import cv2
import random
import pickle
from pathlib import Path
from matplotlib import pyplot as plt

size = 128
# Path to the object detection dataset
object_detection_dataset_path = Path("datasets/CLASS_20_merge")
annotation_files_path = Path("datasets/DIOR_20_Merge_labled/pkl")

normal_image_dataset_path = Path("datasets/DIOR/JPEGImages-trainval")
output_folder = Path(f"datasets/class_20_merge_with_dior_{size}")
image_output_folder = output_folder / "image"
pkl_output_folder = output_folder / "pkl"

# #---------kkuhn-block------------------------------ # recreate folders
# if output_folder.exists():
#     shutil.rmtree(output_folder)
#
# image_output_folder.mkdir(parents=True, exist_ok=True)
# pkl_output_folder.mkdir(parents=True, exist_ok=True)
# #---------kkuhn-block------------------------------

# Fixed size for resizing the images
fixed_size = (size, size)
# add progress bar
from tqdm import tqdm

tbar = tqdm(total=len(list(object_detection_dataset_path.glob("*"))))
# Iterate over the object detection dataset
for image_file in object_detection_dataset_path.glob("*"):
    tbar.update(1)
    # Load the image
    try:
        image = cv2.imread(str(image_file))
    except Exception as e:
        print("corrupted: " + str(image_file))
        continue

    if image_file.name.endswith(".jpg"):
        continue

    # Resize the image to the fixed size
    resized_image = cv2.resize(image, fixed_size)
    # Load the corresponding annotation file
    annotation_file = annotation_files_path / (image_file.stem + ".pkl")
    with open(annotation_file, "rb") as f:
        annotation_data = pickle.load(f)

    normal_image_path = random.choice(list(normal_image_dataset_path.glob("*")))
    normal_image = cv2.imread(str(normal_image_path))

    x_offset = random.randint(0, normal_image.shape[1] - resized_image.shape[1])
    y_offset = random.randint(0, normal_image.shape[0] - resized_image.shape[0])

    normal_image[y_offset:y_offset + resized_image.shape[0], x_offset:x_offset + resized_image.shape[1]] = resized_image

    #---------kkuhn-block------------------------------ # save the image
    modified_image_file = image_output_folder / (image_file.stem + "_mix.jpg")
    cv2.imwrite(str(modified_image_file), normal_image)
    #---------kkuhn-block------------------------------

    # Adjust the bounding box coordinates based on the resizing
    for category_id, (bounding_boxes, confidence) in annotation_data.items():
        for i in range(len(bounding_boxes)):
            x_min, y_min, x_max, y_max = bounding_boxes[i]
            x_min = int(x_min * fixed_size[0] / image.shape[1])
            y_min = int(y_min * fixed_size[1] / image.shape[0])
            x_max = int(x_max * fixed_size[0] / image.shape[1])
            y_max = int(y_max * fixed_size[1] / image.shape[0])
            # add the offset
            x_min += x_offset
            y_min += y_offset
            x_max += x_offset
            y_max += y_offset
            bounding_boxes[i] = (x_min, y_min, x_max, y_max)

    # ---------kkuhn-block------------------------------ # Save the modified annotation file
    modified_annotation_file = pkl_output_folder / (image_file.stem + "_mix.pkl")
    with open(modified_annotation_file, "wb") as f:
        pickle.dump(annotation_data, f)
    # ---------kkuhn-block------------------------------

    # #---------kkuhn-block------------------------------ # stop
    # if tbar.n == 100:
    #     break
    # #---------kkuhn-block------------------------------

    # #---------kkuhn-block------------------------------ # visualize the bounding boxes
    # plt.imshow(cv2.cvtColor(normal_image, cv2.COLOR_BGR2RGB))
    # for bounding_box in bounding_boxes:
    #     x_min, y_min, x_max, y_max = bounding_box
    #     plt.gca().add_patch(plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, edgecolor='r', facecolor='none'))
    #
    # plt.show()
    # #---------kkuhn-block------------------------------
