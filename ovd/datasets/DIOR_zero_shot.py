# import os
# from detectron2.data.datasets.register_coco import register_coco_instances
# from detectron2.data.datasets.builtin_meta import _get_builtin_metadata
# from .lvis_v1 import custom_register_lvis_instances
# from detectron2.data import MetadataCatalog
#
# categories_seen = [
#     {"id": 0, "name": "Airplane"},
#     {"id": 1, "name": "Airport"},
#     {"id": 2, "name": "Baseball field"},
#     {"id": 3, "name": "Basketball court"},
#     {"id": 4, "name": "Bridge"},
#     {"id": 5, "name": "Chimney"},
#     {"id": 6, "name": "Dam"},
#     {"id": 7, "name": "Expressway service area"},
#     {"id": 8, "name": "Expressway toll station"},
#     {"id": 9, "name": "Golf course"},
#     {"id": 10, "name": "Ground track field"},
#     {"id": 11, "name": "Harbor"},
#     {"id": 12, "name": "Overpass"},
#     {"id": 13, "name": "Ship"},
#     {"id": 14, "name": "Stadium"}
# ]
#
# categories_unseen = [
#     # ---------kkuhn-block------------------------------ # from detection datasets
#     {"id": 15, "name": "Storage tank"},
#     {"id": 16, "name": "Tennis court"},
#     {"id": 17, "name": "Train station"},
#     {"id": 18, "name": "Vehicle"},
#     {"id": 19, "name": "Wind mill"},
#     # ---------kkuhn-block------------------------------
#
#     # ---------kkuhn-block------------------------------ # from classification datasets
#     {"id": 20, "name": "agricultural"},
#     {"id": 21, "name": "artificial dense forest land"},
#     {"id": 22, "name": "artificial sparse forest land"},
#     {"id": 23, "name": "bare land"},
#     {"id": 24, "name": "baseball diamond"},
#     {"id": 25, "name": "beach"},
#     {"id": 26, "name": "blue structured factory building"},
#     {"id": 27, "name": "building"},
#     {"id": 28, "name": "cemetery"},
#     {"id": 29, "name": "center"},
#     {"id": 30, "name": "chaparral"},
#     {"id": 31, "name": "christmas tree farm"},
#     {"id": 32, "name": "church"},
#     {"id": 33, "name": "circular farmland"},
#     {"id": 34, "name": "closed road"},
#     {"id": 35, "name": "cloud"},
#     {"id": 36, "name": "coastal mansion"},
#     {"id": 37, "name": "commercial"},
#     {"id": 38, "name": "construction site"},
#     {"id": 39, "name": "cross river bridge"},
#     {"id": 40, "name": "crossroads"},
#     {"id": 41, "name": "crosswalk"},
#     {"id": 42, "name": "dense residential"},
#     {"id": 43, "name": "dense tall building"},
#     {"id": 44, "name": "denseforest"},
#     {"id": 45, "name": "desert"},
#     {"id": 46, "name": "dock"},
#     {"id": 47, "name": "farm land"},
#     {"id": 48, "name": "ferry terminal"},
#     {"id": 49, "name": "fish pond"},
#     {"id": 50, "name": "football field"},
#     {"id": 51, "name": "footbridge"},
#     {"id": 52, "name": "forest"},
#     {"id": 53, "name": "freeway"},
#     {"id": 54, "name": "graff"},
#     {"id": 55, "name": "grass land"},
#     {"id": 56, "name": "high buildings"},
#     {"id": 57, "name": "highway"},
#     {"id": 58, "name": "industrial"},
#     {"id": 59, "name": "intersection"},
#     {"id": 60, "name": "island"},
#     {"id": 61, "name": "lake"},
#     {"id": 62, "name": "low scattered building"},
#     {"id": 63, "name": "low buildings"},
#     {"id": 64, "name": "lrregular farmland"},
#     {"id": 65, "name": "meadow"},
#     {"id": 66, "name": "medium density scattered building"},
#     {"id": 67, "name": "Medium density structured building"},
#     {"id": 68, "name": "medium residential"},
#     {"id": 69, "name": "mobile home park"},
#     {"id": 70, "name": "mountain"},
#     {"id": 71, "name": "natural dense forest land"},
#     {"id": 72, "name": "natural sparse forest land"},
#     {"id": 73, "name": "nursing home"},
#     {"id": 74, "name": "oil gas field"},
#     {"id": 75, "name": "oil tank"},
#     {"id": 76, "name": "oil well"},
#     {"id": 77, "name": "palace"},
#     {"id": 78, "name": "park"},
#     {"id": 79, "name": "parking"},
#     {"id": 80, "name": "parking lot"},
#     {"id": 81, "name": "parking space"},
#     {"id": 82, "name": "plastic greenhouse"},
#     {"id": 83, "name": "playground"},
#     {"id": 84, "name": "pond"},
#     {"id": 85, "name": "port"},
#     {"id": 86, "name": "railway"},
#     {"id": 87, "name": "rectangular farmland"},
#     {"id": 88, "name": "red structured factory building"},
#     {"id": 89, "name": "refinery"},
#     {"id": 90, "name": "regular farmland"},
#     {"id": 91, "name": "residential"},
#     {"id": 92, "name": "resort"},
#     {"id": 93, "name": "river"},
#     {"id": 94, "name": "roads"},
#     {"id": 95, "name": "roundabout"},
#     {"id": 96, "name": "runway"},
#     {"id": 97, "name": "runway marking"},
#     {"id": 98, "name": "scattered blue roof factory building"},
#     {"id": 99, "name": "scattered red roof factory building"},
#     {"id": 100, "name": "school"},
#     {"id": 101, "name": "sea ice"},
#     {"id": 102, "name": "sewage plant type one"},
#     {"id": 103, "name": "sewage plant type two"},
#     {"id": 104, "name": "shipping yard"},
#     {"id": 105, "name": "snowberg"},
#     {"id": 106, "name": "solar panel"},
#     {"id": 107, "name": "solar power station"},
#     {"id": 108, "name": "sparse residential"},
#     {"id": 109, "name": "sparseforest"},
#     {"id": 110, "name": "square"},
#     {"id": 111, "name": "steelworks"},
#     {"id": 112, "name": "storage land"},
#     {"id": 113, "name": "swimming pool"},
#     {"id": 114, "name": "terrace"},
#     {"id": 115, "name": "thermal power plant"},
#     {"id": 116, "name": "thermal power station"},
#     {"id": 117, "name": "transformer station"},
#     {"id": 118, "name": "vegetable plot"},
#     {"id": 119, "name": "viaduct"},
#     {"id": 120, "name": "wastewater treatment plant"},
#     {"id": 121, "name": "water"},
#     {"id": 122, "name": "wetland"},
#     # ---------kkuhn-block------------------------------
# ]
#
# categories_all = [
#     {"id": 0, "name": "Airplane"},
#     {"id": 1, "name": "Airport"},
#     {"id": 2, "name": "Baseball field"},
#     {"id": 3, "name": "Basketball court"},
#     {"id": 4, "name": "Bridge"},
#     {"id": 5, "name": "Chimney"},  # didn't find in classification dataset
#     {"id": 6, "name": "Dam"},  # didn't find in classification dataset
#     {"id": 7, "name": "Expressway service area"},  # didn't find in classification dataset
#     {"id": 8, "name": "Expressway toll station"},  # didn't find in classification dataset
#     {"id": 9, "name": "Golf course"},
#     {"id": 10, "name": "Ground track field"},
#     {"id": 11, "name": "Harbor"},
#     {"id": 12, "name": "Overpass"},
#     {"id": 13, "name": "Ship"},
#     {"id": 14, "name": "Stadium"},
#     {"id": 15, "name": "Storage tank"},
#     {"id": 16, "name": "Tennis court"},
#     {"id": 17, "name": "Train station"},
#     {"id": 18, "name": "Vehicle"},  # didn't find in classification dataset
#     {"id": 19, "name": "Wind mill"},  # didn't find in classification dataset
#
#     {"id": 20, "name": "agricultural"},
#     {"id": 21, "name": "artificial dense forest land"},
#     {"id": 22, "name": "artificial sparse forest land"},
#     {"id": 23, "name": "bare land"},
#     {"id": 24, "name": "baseball diamond"},
#     {"id": 25, "name": "beach"},
#     {"id": 26, "name": "blue structured factory building"},
#     {"id": 27, "name": "building"},
#     {"id": 28, "name": "cemetery"},
#     {"id": 29, "name": "center"},
#     {"id": 30, "name": "chaparral"},
#     {"id": 31, "name": "christmas tree farm"},
#     {"id": 32, "name": "church"},
#     {"id": 33, "name": "circular farmland"},
#     {"id": 34, "name": "closed road"},
#     {"id": 35, "name": "cloud"},
#     {"id": 36, "name": "coastal mansion"},
#     {"id": 37, "name": "commercial"},
#     {"id": 38, "name": "construction site"},
#     {"id": 39, "name": "cross river bridge"},
#     {"id": 40, "name": "crossroads"},
#     {"id": 41, "name": "crosswalk"},
#     {"id": 42, "name": "dense residential"},
#     {"id": 43, "name": "dense tall building"},
#     {"id": 44, "name": "denseforest"},
#     {"id": 45, "name": "desert"},
#     {"id": 46, "name": "dock"},
#     {"id": 47, "name": "farm land"},
#     {"id": 48, "name": "ferry terminal"},
#     {"id": 49, "name": "fish pond"},
#     {"id": 50, "name": "football field"},
#     {"id": 51, "name": "footbridge"},
#     {"id": 52, "name": "forest"},
#     {"id": 53, "name": "freeway"},
#     {"id": 54, "name": "graff"},
#     {"id": 55, "name": "grass land"},
#     {"id": 56, "name": "high buildings"},
#     {"id": 57, "name": "highway"},
#     {"id": 58, "name": "industrial"},
#     {"id": 59, "name": "intersection"},
#     {"id": 60, "name": "island"},
#     {"id": 61, "name": "lake"},
#     {"id": 62, "name": "low scattered building"},
#     {"id": 63, "name": "low buildings"},
#     {"id": 64, "name": "lrregular farmland"},
#     {"id": 65, "name": "meadow"},
#     {"id": 66, "name": "medium density scattered building"},
#     {"id": 67, "name": "medium density structured building"},
#     {"id": 68, "name": "medium residential"},
#     {"id": 69, "name": "mobile home park"},
#     {"id": 70, "name": "mountain"},
#     {"id": 71, "name": "natural dense forest land"},
#     {"id": 72, "name": "natural sparse forest land"},
#     {"id": 73, "name": "nursing home"},
#     {"id": 74, "name": "oil gas field"},
#     {"id": 75, "name": "oil tank"},
#     {"id": 76, "name": "oil well"},
#     {"id": 77, "name": "palace"},
#     {"id": 78, "name": "park"},
#     {"id": 79, "name": "parking"},
#     {"id": 80, "name": "parking lot"},
#     {"id": 81, "name": "parking space"},
#     {"id": 82, "name": "plastic greenhouse"},
#     {"id": 83, "name": "playground"},
#     {"id": 84, "name": "pond"},
#     {"id": 85, "name": "port"},
#     {"id": 86, "name": "railway"},
#     {"id": 87, "name": "rectangular farmland"},
#     {"id": 88, "name": "red structured factory building"},
#     {"id": 89, "name": "refinery"},
#     {"id": 90, "name": "regular farmland"},
#     {"id": 91, "name": "residential"},
#     {"id": 92, "name": "resort"},
#     {"id": 93, "name": "river"},
#     {"id": 94, "name": "roads"},
#     {"id": 95, "name": "roundabout"},
#     {"id": 96, "name": "runway"},
#     {"id": 97, "name": "runway marking"},
#     {"id": 98, "name": "scattered blue roof factory building"},
#     {"id": 99, "name": "scattered red roof factory building"},
#     {"id": 100, "name": "school"},
#     {"id": 101, "name": "sea ice"},
#     {"id": 102, "name": "sewage plant type one"},
#     {"id": 103, "name": "sewage plant type two"},
#     {"id": 104, "name": "shipping yard"},
#     {"id": 105, "name": "snowberg"},
#     {"id": 106, "name": "solar panel"},
#     {"id": 107, "name": "solar power station"},
#     {"id": 108, "name": "sparse residential"},
#     {"id": 109, "name": "sparseforest"},
#     {"id": 110, "name": "square"},
#     {"id": 111, "name": "steelworks"},
#     {"id": 112, "name": "storage land"},
#     {"id": 113, "name": "swimming pool"},
#     {"id": 114, "name": "terrace"},
#     {"id": 115, "name": "thermal power plant"},
#     {"id": 116, "name": "thermal power station"},
#     {"id": 117, "name": "transformer station"},
#     {"id": 118, "name": "vegetable plot"},
#     {"id": 119, "name": "viaduct"},
#     {"id": 120, "name": "wastewater treatment plant"},
#     {"id": 121, "name": "water"},
#     {"id": 122, "name": "wetland"},
#     # ---------kkuhn-block------------------------------
# ]
#
#
# def _get_metadata(cat):
#     if cat == 'all':
#         # return _get_builtin_metadata('coco')
#         id_to_name = {x['id']: x['name'] for x in categories_all}
#     elif cat == 'seen':
#         id_to_name = {x['id']: x['name'] for x in categories_seen}
#     else:
#         assert cat == 'unseen'
#         id_to_name = {x['id']: x['name'] for x in categories_unseen}
#
#     thing_dataset_id_to_contiguous_id = {
#         x: i for i, x in enumerate(sorted(id_to_name))}
#     thing_classes = [id_to_name[k] for k in sorted(id_to_name)]
#     return {
#         "thing_dataset_id_to_contiguous_id": thing_dataset_id_to_contiguous_id,
#         "thing_classes": thing_classes}
#
#
# _PREDEFINED_SPLITS_COCO = {
#     "DIOR_zeroshot_train": ("DIOR/JPEGImages-trainval", "DIOR/Annotations/coco_split/instances_DIOR_train_seen_2.json", 'seen'),
#     "DIOR_zeroshot_val": ("DIOR/JPEGImages-test", "DIOR/Annotations/coco_split/instances_DIOR_test_unseen_2.json", 'unseen'),
#     "DIOR_not_zeroshot_val": ("DIOR/JPEGImages-test", "DIOR/Annotations/coco_split/instances_DIOR_test_seen_2.json", 'seen'),
#     "DIOR_generalized_zeroshot_val": ("DIOR/JPEGImages-test", "DIOR/Annotations/coco_split/instances_DIOR_test_all_2_oriorder.json", 'all'),
#     "DIOR_zeroshot_train_oriorder": (
#         "DIOR/JPEGImages-trainval", "DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder.json", 'all'),
#     "DIOR_test": ("DIOR/JPEGImages-test", "DIOR/DIOR_test.json", 'all'),
#     "DIOR_train": ("DIOR/JPEGImages-test", "DIOR/DIOR_train.json", 'all'),
# }
#
# for key, (image_root, json_file, cat) in _PREDEFINED_SPLITS_COCO.items():
#     register_coco_instances(
#         key,
#         _get_metadata(cat),
#         os.path.join("datasets", json_file) if "://" not in json_file else json_file,
#         os.path.join("datasets", image_root),
#     )


import os
from detectron2.data.datasets.register_coco import register_coco_instances
from detectron2.data.datasets.builtin_meta import _get_builtin_metadata
from .lvis_v1 import custom_register_lvis_instances
from detectron2.data import MetadataCatalog

categories_seen = [{"id": 0, "name": "Airplane"},
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
                  {"id": 14, "name": "Stadium"}
                  ]

categories_unseen = [
    {"id": 15, "name": "Storage tank"},
    {"id": 16, "name": "Tennis court"},
    {"id": 17, "name": "Train station"},
    {"id": 18, "name": "Vehicle"},
    {"id": 19, "name": "Wind mill"}
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
    "DIOR_zeroshot_train": ("DIOR/JPEGImages-trainval", "DIOR/Annotations/coco_split/instances_DIOR_train_seen_2.json", 'seen'),
    "DIOR_zeroshot_val": ("DIOR/JPEGImages-test", "DIOR/Annotations/coco_split/instances_DIOR_test_unseen_2.json", 'unseen'),
    "DIOR_not_zeroshot_val": ("DIOR/JPEGImages-test", "DIOR/Annotations/coco_split/instances_DIOR_test_seen_2.json", 'seen'),
    "DIOR_generalized_zeroshot_val": ("DIOR/JPEGImages-test", "DIOR/Annotations/coco_split/instances_DIOR_test_all_2_oriorder_ori.json", 'all'),
    "DIOR_zeroshot_train_oriorder": (
        "DIOR/JPEGImages-trainval", "DIOR/Annotations/coco_split/instances_DIOR_train_seen_2_oriorder.json", 'all'),
    "DIOR_test": ("DIOR/JPEGImages-test", "DIOR/DIOR_test.json", 'all'),
    "DIOR_train": ("DIOR/JPEGImages-test", "DIOR/DIOR_train.json", 'all'),
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
