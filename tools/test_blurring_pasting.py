import cv2
import numpy as np

one_image_path = "/data/pcl/proj/object-centric-ovd/datasets/CLASS_20_merge/0_airplane,aircraft,aeroplane_1000.jpg"
second_image_path = "/data/pcl/proj/object-centric-ovd/datasets/CLASS_20_merge/0_airplane,aircraft,aeroplane_10.jpg"

# #---------kkuhn-block------------------------------ # version 1
# # 读取原始图像和大图
# image = cv2.imread(one_image_path)
# background = cv2.imread(second_image_path)
#
# image = cv2.resize(image, (500, 500))
# background = cv2.resize(background, (800, 800))
#
#
# # 创建一个掩膜，用于羽化图像的边缘
# mask = np.zeros(image.shape[:2], dtype=np.uint8)
# cv2.rectangle(mask, (0, 0), (image.shape[1], image.shape[0]), (255), thickness=10)
# blur = cv2.GaussianBlur(mask, (51, 51), 0)
#
# # 对图像进行羽化处理
# blurred_image = cv2.addWeighted(image, 0.7, cv2.cvtColor(blur, cv2.COLOR_GRAY2BGR), 0.3, 0)
#
# # 将羽化后的图像贴到大图上
# x_offset = 100  # 在大图上的x轴偏移量
# y_offset = 200  # 在大图上的y轴偏移量
# background[y_offset:y_offset + image.shape[0], x_offset:x_offset + image.shape[1]] = blurred_image
#
# # 显示结果
# # cv2.imshow('Result', background)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()
#
# # show with plt convert the data type if necessary
#
# import matplotlib.pyplot as plt
#
# plt.imshow(background)
# plt.show()
# #---------kkuhn-block------------------------------


# #---------kkuhn-block------------------------------ # version 2
# import cv2
# import numpy as np
#
# # 读取大图和小图
# background = cv2.imread(one_image_path)
# foreground = cv2.imread(second_image_path)
#
# # 将小图调整为与大图相同的大小
# foreground_resized = cv2.resize(foreground, (background.shape[1], background.shape[0]))
#
# # 创建一个与大图相同大小的掩膜（mask）
# mask = np.zeros(background.shape, dtype=np.uint8)
#
# # 在掩膜上绘制小图的轮廓
# gray_foreground = cv2.cvtColor(foreground_resized, cv2.COLOR_BGR2GRAY)
# ret, threshold = cv2.threshold(gray_foreground, 10, 255, cv2.THRESH_BINARY)
# contours, hierarchy = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(mask, contours, -1, (255, 255, 255), thickness=cv2.FILLED)
#
# # 使用高斯模糊对掩膜进行羽化处理
# blurred_mask = cv2.GaussianBlur(mask, (21, 21), 0)
#
# # 将羽化后的小图与大图进行融合
# alpha = 0.6  # 控制融合程度
# beta = 1.0 - alpha
# blended = cv2.addWeighted(background, alpha, blurred_mask, beta, 0)
#
# # 将小图贴到大图上
# result = cv2.bitwise_and(blended, mask)
#
# # plt
# import matplotlib.pyplot as plt
#
# plt.imshow(result)
# plt.show()
# #---------kkuhn-block------------------------------


# #---------kkuhn-block------------------------------ # version 4
#
# # 读取原始图像
# image = cv2.imread(one_image_path)
#
# # 创建一个与原始图像相同大小的透明图像
# alpha = np.zeros(image.shape[:2], dtype=np.uint8)
#
# # 创建一个椭圆形的掩码，用于羽化边缘
# mask = np.zeros(image.shape[:2], dtype=np.uint8)
# center = (image.shape[1] // 2, image.shape[0] // 2)  # 图像中心点
# axes = (image.shape[1] // 2, image.shape[0] // 2)  # 椭圆轴长
# cv2.ellipse(mask, center, axes, 0, 0, 360, 255, -1)
#
# # 使用高斯模糊对掩码进行羽化
# blurred_mask = cv2.GaussianBlur(mask, (51, 51), 0)
#
# # 将羽化后的掩码赋值给透明图像的alpha通道
# alpha[:, :] = blurred_mask
#
# # 将透明图像与原始图像合并
# result = cv2.merge((image, alpha))
#
#
# # save to png
# cv2.imwrite("../rubb/alpha.png", result)
#
# #---------kkuhn-block------------------------------


# ---------kkuhn-block------------------------------ # version 5

# Read the original image
image = cv2.imread(one_image_path)

# Create a transparent image with the same size as the original image
alpha = np.zeros(image.shape[:2], dtype=np.uint8)

# Create a rectangular mask for feathering the edges
mask = np.zeros(image.shape[:2], dtype=np.uint8)
rectangle_size = (image.shape[1] - 20, image.shape[0] - 20)  # Size of the rectangle (slightly smaller than the image)
rectangle_position = (10, 10)  # Position of the rectangle
cv2.rectangle(mask, rectangle_position, (rectangle_position[0] + rectangle_size[0], rectangle_position[1] + rectangle_size[1]), 255, -1)

# Apply Gaussian blur to the mask for feathering
blurred_mask = cv2.GaussianBlur(mask, (51, 51), 0)

# Assign the feathered mask to the alpha channel of the transparent image
alpha[:, :] = blurred_mask

# Merge the transparent image with the original image
result = cv2.merge((image, alpha))

# Save the resulting image
cv2.imwrite('../rubb/alpha1.png', result)

# ---------kkuhn-block------------------------------

# ---------kkuhn-block------------------------------ # version 6: merge the transparent part and the pasted part

# Read the original image
image = cv2.imread(one_image_path)
background = cv2.imread(second_image_path)

image = cv2.resize(image, (500, 500))
background = cv2.resize(background, (800, 800))
# add alpha channel
background = cv2.cvtColor(background, cv2.COLOR_BGR2BGRA)

# Create a transparent image with the same size as the original image
alpha = np.zeros(image.shape[:2], dtype=np.uint8)

# Create a rectangular mask for feathering the edges
mask = np.zeros(image.shape[:2], dtype=np.uint8)
rectangle_size = (image.shape[1], image.shape[0])  # Size of the rectangle (slightly smaller than the image)
rectangle_position = (0, 0)  # Position of the rectangle
cv2.rectangle(mask, rectangle_position, (rectangle_position[0] + rectangle_size[0], rectangle_position[1] + rectangle_size[1]), 255, -1)

# Apply Gaussian blur to the mask for feathering
blurred_mask = cv2.GaussianBlur(mask, (51, 51), 0)

# Assign the feathered mask to the alpha channel of the transparent image
alpha[:, :] = blurred_mask

# Merge the transparent image with the original image
result = cv2.merge((image, alpha))


x_offset = 100
y_offset = 200
background[y_offset:y_offset + image.shape[0], x_offset:x_offset + image.shape[1]] = result

cv2.imwrite('../rubb/alpha3.png', background)

# ---------kkuhn-block------------------------------
