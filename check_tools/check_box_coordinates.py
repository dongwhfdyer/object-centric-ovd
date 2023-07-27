import os
import pickle
from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt

file_path = "datasets/DIOR_20_Merge_labled/pkl/4_bridge_1.pkl"

with open(file_path, "rb") as f:
    data = pickle.load(f)
    boxes_coordinates = data[4][0]
    print("--------------------------------------------------")

img_path = "datasets/DIOR_20_Merge/4_bridge_1.jpg"
output_dir = 'rubb/visualized'
img_file_name = '0_airplane,aircraft,aeroplane_1.jpg'


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


visualized_img = visualize_boxes(img_path, boxes_coordinates)
plt.imshow(visualized_img)
plt.show()


visualized_img.save(os.path.join(output_dir, img_file_name))
