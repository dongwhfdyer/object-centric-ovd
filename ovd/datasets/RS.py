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
    "rs": ("remote_sensing/RS_images", "remote_sensing/annotations/image_info.json"),
    "rs_pis": ("remote_sensing/RS_images", "remote_sensing/annotations/rs_pis_aggregated.json"),
}

for key, (image_root, json_file) in _CUSTOM_SPLITS_IMAGENET.items():
    custom_register_imagenet_instances(
        key,
        get_lvis_instances_meta('lvis_v1'),
        os.path.join("datasets", json_file) if "://" not in json_file else json_file,
        os.path.join("datasets", image_root),
    )
