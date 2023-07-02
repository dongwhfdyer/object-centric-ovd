# kuhn notes

# Critical issues

the 

As for `tools/unzip_imagenet_lvis.py` file, we added the feature for selecting the overlapping images between imagenet and lvis dataset. 
And we create a directory that contains the overlapping images by sim-linking the images from original imagenet directory.


## eval 

`python train_net.py --num-gpus 1 --config-file configs/rs/RS_OVD_Base_PIS_only_20_dior_automatic.yaml --eval-only MODEL.WEIGHTS output/rs_dior_automatic_ovd_PIS/model_0049999.pth`