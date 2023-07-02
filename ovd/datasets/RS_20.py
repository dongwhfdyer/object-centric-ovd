import os

from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.data.datasets.lvis import get_lvis_instances_meta
from .lvis_v1 import custom_load_lvis_json


def custom_register_imagenet_instances(name, metadata, json_file, image_root):
    """
    """
    DatasetCatalog.register(name, lambda: custom_load_lvis_json(
        json_file, image_root, name))
    MetadataCatalog.get(name).set(
        json_file=json_file, image_root=image_root,
        evaluator_type="imagenet", **metadata
    )


_CUSTOM_SPLITS_IMAGENET = {
    "rs_20": ("remote_sensing/RS_images_20", "remote_sensing/annotations/rs_20_image_info.json"),
    # "rs_pis_20": ("remote_sensing/RS_images_20", "remote_sensing/annotations/rs_20_pis_aggregated.json"),
    "rs_pis_20_merge": ("CLASS_20_merge", "DIOR_20_Merge_labled/20_merge_image_info.json"),
    "dior_automatic": ("DIOR_automatic_label/orig_images", "DIOR_automatic_label/DIOR_automatic_image_info.json"),
}

for key, (image_root, json_file) in _CUSTOM_SPLITS_IMAGENET.items():
    custom_register_imagenet_instances(
        key,
        get_lvis_instances_meta('lvis_v1'),
        os.path.join("datasets", json_file) if "://" not in json_file else json_file,
        os.path.join("datasets", image_root),
    )
