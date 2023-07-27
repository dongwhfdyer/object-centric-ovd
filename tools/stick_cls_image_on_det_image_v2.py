# import json
# import pickle
# from pathlib import Path
#
# import cv2
#
# cls_image = Path("datasets/remote_sensing/RS_images/bridge/4_00000001.jpg")
# cls_pkl = Path("datasets/MAVL_proposals/rs_props/class_specific/4/4_00000001.pkl")
#
# det_image = Path("datasets/DIOR_automatic_label/orig_images/00011.jpg")
# det_pkl = Path("datasets/DIOR_automatic_label/pkl/00011.pkl")
#
# with open(cls_pkl, 'rb') as f:
#     anno = pickle.load(f)
#     bounding_box = anno[4][0][0]
#     x_min, y_min, x_max, y_max = bounding_box
#
# with open(det_pkl, 'rb') as f:
#     anno = pickle.load(f)
#     bounding_box = anno[4][0][0]
#     x_min, y_min, x_max, y_max = bounding_box
#
# # # cls: read image, boundingbox, and label
# # cls_image =cv2.imread(str(cls_image_path))
# #
# #
# # # det: read image, boundingbox, and label
# # det_image =cv2.imread(str(det_image_path))

# #---------kkuhn-block------------------------------ # version 1
# import pickle
#
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
#
# # Load the images
# cls_image = cv2.imread("datasets/remote_sensing/RS_images/bridge/4_00000001.jpg")
# det_image = cv2.imread("datasets/DIOR_automatic_label/orig_images/00011.jpg")
#
# # Load the bounding box coordinates
# with open("datasets/MAVL_proposals/rs_props/class_specific/4/4_00000001.pkl", 'rb') as f:
#     cls_anno = pickle.load(f)
#     cls_bounding_box = cls_anno[4][0][0]
#     cls_x_min, cls_y_min, cls_x_max, cls_y_max = cls_bounding_box
#
# with open("datasets/DIOR_automatic_label/pkl/00011.pkl", 'rb') as f:
#     det_anno = pickle.load(f)
#     det_bounding_box = det_anno[0][0][0]
#     det_x_min, det_y_min, det_x_max, det_y_max = det_bounding_box
#
# # Calculate the rotation angle and scale factors
# rotation_angle = 45  # Specify the rotation angle in degrees
# scale_factor = 0.3  # Specify the scale factor
#
# # Rotate the cls_image
# (h, w) = cls_image.shape[:2]
# center = (w // 2, h // 2)
# M = cv2.getRotationMatrix2D(center, rotation_angle, scale_factor)
# rotated_cls_image = cv2.warpAffine(cls_image, M, (w, h))
#
# # Scale the det_image
# scaled_det_image = cv2.resize(det_image, None, fx=scale_factor, fy=scale_factor)
#
# # Adjust the bounding box coordinates for rotation and scale
# def transform_coordinates(x, y, angle, scale_factor, center):
#     # Translate the coordinates to the origin
#     translated_x = x - center[0]
#     translated_y = y - center[1]
#
#     # Rotate the coordinates
#     rotated_x = translated_x * np.cos(np.deg2rad(angle)) - translated_y * np.sin(np.deg2rad(angle))
#     rotated_y = translated_x * np.sin(np.deg2rad(angle)) + translated_y * np.cos(np.deg2rad(angle))
#
#     # Scale the coordinates
#     scaled_x = rotated_x * scale_factor
#     scaled_y = rotated_y * scale_factor
#
#     # Translate the coordinates back to the original position
#     transformed_x = scaled_x + center[0]
#     transformed_y = scaled_y + center[1]
#
#     return int(transformed_x), int(transformed_y)
#
# # Transform the bounding box coordinates for cls_image
# transformed_cls_x_min, transformed_cls_y_min = transform_coordinates(cls_x_min, cls_y_min, rotation_angle, scale_factor, center)
# transformed_cls_x_max, transformed_cls_y_max = transform_coordinates(cls_x_max, cls_y_max, rotation_angle, scale_factor, center)
#
# # Overlay the transformed cls_image onto the det_image
# overlay_image = np.copy(scaled_det_image)
# overlay_image[transformed_cls_y_min:transformed_cls_y_max, transformed_cls_x_min:transformed_cls_x_max] = rotated_cls_image
#
# # Visualize the result
# plt.imshow(cv2.cvtColor(overlay_image, cv2.COLOR_BGR2RGB))
# plt.show()
# #---------kkuhn-block------------------------------

# ---------kkuhn-block------------------------------ # version 2
import cv2
import matplotlib.pyplot as plt
import json
import pickle
from pathlib import Path

cls_image_path = Path("datasets/remote_sensing/RS_images/bridge/4_00000001.jpg")
cls_pkl_path = Path("datasets/MAVL_proposals/rs_props/class_specific/4/4_00000001.pkl")

det_image_path = Path("datasets/DIOR_automatic_label/orig_images/00011.jpg")
det_pkl_path = Path("datasets/DIOR_automatic_label/pkl/00011.pkl")

# Load cls_image
cls_image = cv2.imread(str(cls_image_path))

# Perform scaling and rotation on cls_image
scale_percent = 60  # adjust the scale as needed
width = int(cls_image.shape[1] * scale_percent / 100)
height = int(cls_image.shape[0] * scale_percent / 100)
dim = (width, height)
cls_image = cv2.resize(cls_image, dim, interpolation=cv2.INTER_AREA)
angle = 0  # adjust the rotation angle as needed
rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
cls_image = cv2.warpAffine(cls_image, rotation_matrix, (width, height))

# Load bounding box coordinates from cls_pkl
with open(cls_pkl_path, 'rb') as f:
    anno = pickle.load(f)
    bounding_box = anno[4][0][0]
    x_min, y_min, x_max, y_max = bounding_box

# Adjust bounding box coordinates based on scaling and rotation
x_min = int(x_min * scale_percent / 100)
y_min = int(y_min * scale_percent / 100)
x_max = int(x_max * scale_percent / 100)
y_max = int(y_max * scale_percent / 100)

# Load det_image
det_image = cv2.imread(str(det_image_path))

# Overlay cls_image onto det_image
x_offset = 100  # adjust the x-offset as needed
y_offset = 100  # adjust the y-offset as needed
det_image[y_offset:y_offset + cls_image.shape[0], x_offset:x_offset + cls_image.shape[1]] = cls_image

# Adjust bounding box coordinates based on overlay position
x_min += x_offset
x_max += x_offset
y_min += y_offset
y_max += y_offset

# Convert BGR image to RGB for plt visualization
det_image_rgb = cv2.cvtColor(det_image, cv2.COLOR_BGR2RGB)

# Display the result using plt
plt.imshow(det_image_rgb)
plt.axis('off')

# Draw bounding box on the det_image_rgb
plt.plot([x_min, x_max, x_max, x_min, x_min], [y_min, y_min, y_max, y_max, y_min], color='red', linewidth=3)



# Show the image
plt.show()

# ---------kkuhn-block------------------------------
