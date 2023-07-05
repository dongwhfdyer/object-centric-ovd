# kuhn notes

# Critical issues

the 

As for `tools/unzip_imagenet_lvis.py` file, we added the feature for selecting the overlapping images between imagenet and lvis dataset. 
And we create a directory that contains the overlapping images by sim-linking the images from original imagenet directory.


## eval 

`python train_net.py --num-gpus 1 --config-file configs/rs/RS_OVD_Base_PIS_only_20_dior_automatic.yaml --eval-only MODEL.WEIGHTS output/rs_dior_automatic_ovd_PIS/model_0049999.pth`

## how to split seen and unseen

  TRAIN: ("DIOR_zeroshot_train_oriorder", "dior_automatic")
    "DIOR_zeroshot_train_oriorder": ( "DIOR/JPEGImages-trainval", "DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder.json", 'all'),

unseen classes: Storage tank, Tennis court,train station, vehicle, wind mill

if I want to set the above classes as the unseen classes. I need to only use the images from other classes in the `instances_DIOR_train_seen_2_oriorder.json` file.
And in `instances_DIOR_train_seen_2_oriorder_cat_info.json` file, the `image_count` for the above unseen classes should be set to 0.

