import cv2
import numpy as np

one_image_path = "/data/pcl/proj/object-centric-ovd/datasets/CLASS_20_merge/0_airplane,aircraft,aeroplane_1000.jpg"
second_image_path = "/data/pcl/proj/object-centric-ovd/datasets/CLASS_20_merge/0_airplane,aircraft,aeroplane_10.jpg"

image = cv2.imread(one_image_path)
image = cv2.resize(image, (100, 100))
black = np.zeros((80, 80, 3), dtype=np.uint8)

background = cv2.imread(second_image_path)

background_mask = np.zeros_like(background)
# stick the image on the background_mask
x_offset = 100
y_offset = 100
background_mask[y_offset:y_offset + image.shape[0], x_offset:x_offset + image.shape[1]] = image

background_mask_mask = np.ones_like(background_mask)
background_mask_mask[y_offset + 10:y_offset + black.shape[0] + 10, x_offset + 10:x_offset + black.shape[1] + 10] = 0
background_mask_mask = 1 - background_mask_mask
background_mask_mask = background_mask_mask * 255

# background_mask_mask[background_mask == 0] = 0
background_mask_mask_blur = cv2.GaussianBlur(background_mask_mask, (77, 77), 0)
cv2.imwrite('../rubb/background_mask_mask_blur.png', background_mask_mask_blur)

background_mask_mask_blur_weights = background_mask_mask_blur / 255.0

res = background_mask * background_mask_mask_blur_weights + background * (1 - background_mask_mask_blur_weights)
cv2.imwrite('../rubb/res.png', res)


def resize_and_copy_image(image, big_image):
    # scale = 0.8
    # resized_image = cv2.resize(image, None, fx=scale, fy=scale)
    resized_image = image

    background = np.zeros_like(big_image)

    start_x = int((background.shape[1] - resized_image.shape[1]) / 2)
    start_y = int((background.shape[0] - resized_image.shape[0]) / 2)

    background[start_y:start_y + resized_image.shape[0], start_x:start_x + resized_image.shape[1]] = resized_image

    return background
