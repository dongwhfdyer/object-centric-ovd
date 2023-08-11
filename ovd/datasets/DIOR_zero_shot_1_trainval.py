import os
from detectron2.data.datasets.register_coco import register_coco_instances
from detectron2.data.datasets.builtin_meta import _get_builtin_metadata
from .lvis_v1 import custom_register_lvis_instances
from detectron2.data import MetadataCatalog

categories_seen = [{"id": 0, "name": "Airplane"},
                   {"id": 1, "name": "Airport"},
                   {"id": 6, "name": "Dam"},
                   {"id": 7, "name": "Expressway service area"},
                   {"id": 8, "name": "Expressway toll station"},
                   {"id": 9, "name": "Golf course"},
                   {"id": 10, "name": "Ground track field"},
                   {"id": 11, "name": "Harbor"},
                   {"id": 12, "name": "Overpass"},
                   {"id": 14, "name": "Stadium"},
                   {"id": 15, "name": "Storage tank"},
                   {"id": 16, "name": "Tennis court"},
                   {"id": 17, "name": "Train station"},
                   {"id": 18, "name": "Vehicle"},
                   {"id": 19, "name": "Wind mill"}
                   ]

categories_unseen = [
    {"id": 2, "name": "Baseball field"},
    {"id": 3, "name": "Basketball court"},
    {"id": 4, "name": "Bridge"},
    {"id": 5, "name": "Chimney"},
    {"id": 13, "name": "Ship"}

]

categories_all = [{"id": 0, "name": "Airplane"},
                  {"id": 1, "name": "Airport"},
                  {"id": 2, "name": "Baseball field"},
                  {"id": 3, "name": "Basketball court"},
                  {"id": 4, "name": "Bridge"},
                  {"id": 5, "name": "Chimney"},
                  {"id": 6, "name": "Dam"},
                  {"id": 7, "name": "Expressway service area"},
                  {"id": 8, "name": "Expressway toll station"},
                  {"id": 9, "name": "Golf course"},
                  {"id": 10, "name": "Ground track field"},
                  {"id": 11, "name": "Harbor"},
                  {"id": 12, "name": "Overpass"},
                  {"id": 13, "name": "Ship"},
                  {"id": 14, "name": "Stadium"},
                  {"id": 15, "name": "Storage tank"},
                  {"id": 16, "name": "Tennis court"},
                  {"id": 17, "name": "Train station"},
                  {"id": 18, "name": "Vehicle"},
                  {"id": 19, "name": "Wind mill"}
                  ]


def _get_metadata(cat):
    if cat == 'all':
        # return _get_builtin_metadata('coco')
        id_to_name = {x['id']: x['name'] for x in categories_all}
    elif cat == 'seen':
        id_to_name = {x['id']: x['name'] for x in categories_seen}
    else:
        assert cat == 'unseen'
        id_to_name = {x['id']: x['name'] for x in categories_unseen}

    thing_dataset_id_to_contiguous_id = {
        x: i for i, x in enumerate(sorted(id_to_name))}
    thing_classes = [id_to_name[k] for k in sorted(id_to_name)]
    return {
        "thing_dataset_id_to_contiguous_id": thing_dataset_id_to_contiguous_id,
        "thing_classes": thing_classes}


_PREDEFINED_SPLITS_COCO = {
    "DIOR_zeroshot_train_1_trainval": (
    "DIOR/JPEGImages-trainval", "DIOR/Annotations/coco_split/split_1_trainval/instances_DIOR_train_seen_2.json", 'seen'),
    "DIOR_zeroshot_val_1_trainval": (
    "DIOR/JPEGImages-test", "DIOR/Annotations/coco_split/split_1_trainval/instances_DIOR_test_unseen_2.json", 'unseen'),
    "DIOR_not_zeroshot_val_1_trainval": (
    "DIOR/JPEGImages-test", "DIOR/Annotations/coco_split/split_1_trainval/instances_DIOR_test_seen_2.json", 'seen'),
    "DIOR_generalized_zeroshot_val_1_trainval": (
    "DIOR/JPEGImages", "DIOR/Annotations/coco_split/split_1_trainval/instances_DIOR_test_all_2_oriorder_ori.json", 'all'),
    "DIOR_zeroshot_train_oriorder_1_trainval": (
        "DIOR/JPEGImages", "DIOR/Annotations/coco_split/split_1_trainval/instances_DIOR_train_seen_2_oriorder_ori.json", 'all'),
    "DIOR_test_1_trainval": ("DIOR/JPEGImages", "DIOR/Annotations/DIOR_test_coco.json", 'all'),
    "DIOR_train_1_trainval": ("DIOR/JPEGImages", "DIOR/Annotations/DIOR_trainval_coco.json", 'all'),
    "5images": ("5images/images", "5images/fake_coco_annotation.json", 'all'),
}
# metadata = MetadataCatalog.get('coco')
# del metadata.thing_classes
for key, (image_root, json_file, cat) in _PREDEFINED_SPLITS_COCO.items():
    register_coco_instances(
        key,
        _get_metadata(cat),
        os.path.join("datasets", json_file) if "://" not in json_file else json_file,
        os.path.join("datasets", image_root),
    )

# _CUSTOM_SPLITS_COCO = {
#     "coco_caption_train_tags": ("coco/train2017/", "coco/annotations/captions_train2017_tags_allcaps_pis.json"),
#     "coco_caption_val_tags": ("coco/val2017/", "coco/annotations/captions_val2017_tags_allcaps.json"), }
#
# for key, (image_root, json_file) in _CUSTOM_SPLITS_COCO.items():
#     custom_register_lvis_instances(
#         key,
#         _get_builtin_metadata('coco'),
#         os.path.join("datasets", json_file) if "://" not in json_file else json_file,
#         os.path.join("datasets", image_root),
#     )
