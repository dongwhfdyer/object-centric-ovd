import os
import pickle
import shutil
from pathlib import Path

import matplotlib.pyplot as plt

#---------kkuhn-block------------------------------ # input 1
object_detection_dataset_path = Path("datasets/CLASS_20_merge")
annotation_files_path = Path("datasets/DIOR_20_Merge_labled/pkl")
#---------kkuhn-block------------------------------

# #---------kkuhn-block------------------------------ # input 2
# object_detection_dataset_path = Path("datasets/class_20_merge_with_dior/image")
# annotation_files_path = Path("datasets/class_20_merge_with_dior/pkl")
# #---------kkuhn-block------------------------------




output_dir = Path('rubb/visualized')
if output_dir.exists():
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

show_num = 0

for image_file in object_detection_dataset_path.glob("*.jpg"):
    image = plt.imread(str(image_file))
    annotation_file = annotation_files_path / (image_file.stem + ".pkl")
    with open(annotation_file, "rb") as f:
        annotation_data = pickle.load(f)
    plt.imshow(image)
    current_axis = plt.gca()
    # no axis in saving image
    plt.axis('off')
    for category_id, (bounding_boxes, confidence) in annotation_data.items():
        for i in range(len(bounding_boxes)):
            x_min, y_min, x_max, y_max = bounding_boxes[i]

            # Draw bounding box on the image
            current_axis.add_patch(plt.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, color='green', linewidth=2, fill=False))
            # Draw label
            label = f"{category_id} "
            current_axis.text(x_min, y_min - 10, label, color='green', size='medium', backgroundcolor='black')

    # Save the modified image to the output directory
    output_file = output_dir / image_file.name

    plt.savefig(str(output_file))
    plt.close()

    show_num += 1
    if show_num > 100:
        break
