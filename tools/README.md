## The curation of rs datasets

the general steps in summary:

1. after unzipping the rs datasets' images
2. We need to rename the folder name: replace the space with `_`. We need to rename the image name under every subfolder for their chaotic name.
3. Count the number of images in every subfolder, record the number of images of each category, and save them later in the json file.

steps to generate the json files:

1. `python create_rs_imagenet_json.py`. It will generate `image_info.json`, `id2category.json`, `category2id.json`.
2. `python tools/get_ils_labels.py -ckpt saved_models/MDef_DETR_r101_epoch20.pth -dataset rs -dataset_dir datasets/remote_sensing -output datasets/MAVL_proposals/rs_props/class_specific/`
   to generate pseudo labels under `datasets/MAVL_proposals/rs_props/class_specific/`.
3. `python tools/create_lvis_ils_json.py -dataset_dir datasets/remote_sensing -prop_path datasets/MAVL_proposals/rs_props/class_specific -target_path datasets/remote_sensing/annotations/rs_pis_aggregated.json`
   to generate `rs_pis_aggregated.json` which simply aggregate the pseudo labels and the original labels to one json file.

## It's the chatgpt prompt generate for `create_rs_imagenet.py` in `tools` folder.

It's the dataset sturcture. The subfolder's name is the category name.

```

- apple tree
    - 1.jpg
    - 2.jpg
    - ...
- pineapple
    - 1.jpg
    - 2.jpg
    - ...
- paper
    - 1.jpg
    - 2.jpg
    - ...
      ...

```

I want to help me write a piece of code to process the data and generate two json file.
One json file saves the mapping from `category_id` and `category_name`. Both direction should be included.
Another json file saves the image info. The format is shown as follows.
So, generally, the process should be like this.

1. preprocess the image folder name: delete the `space` in the name.
2. Generate `category_id` for each`category_name` and create the corresponding mapping which should include both direction.
3. Iterate over every image in every subfolder. Generate id to `id` field, record image path to `file_name` field, record `category_id` to `pos_category_ids` field, check out the image width and height and save them to `width` and `height` field.

```

{"id": 866847, "file_name": "n04225987/n04225987_2911.JPEG", "pos_category_ids": [962], "width": 332, "height": 500}, {"id": 866848, "file_name": "n04225987/n04225987_2915.JPEG", "pos_category_ids": [962], "width": 400, "height": 500}, {"id": 866849, "file_name": "n04225987/n04225987_2916.JPEG", "pos_category_ids": [962], "width": 500, "height": 375}, {"id": 866850, "file_name": "
n04225987/n04225987_2918.JPEG", "pos_category_ids": [962], "width": 393, "height": 500},...
}

```

I have write some pseudo code for you. Based on the pseudo code and the above instruction, help me write the code.

```

dataset_folder ='datasets/remote_sence_imagenet'

for f in dataset_folder:
# rename the folder name: delete the space
pass

category2id = {}
id2category = {}
for f in dataset_folder:
# generate the category_id for each folder and generate the mapping
pass

# save them to json file

image_info = {}
for f in dataset_folder:
for img in f:
# generate the id, file_name, category_id, width, height. And save them to image_info
pass

# save them to json file

```