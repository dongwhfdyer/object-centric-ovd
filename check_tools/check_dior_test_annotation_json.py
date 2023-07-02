# DIOR_generalized_zeroshot_val
import json
from pathlib import Path

dior_test_json = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_test_all_2_oriorder_ori.json")

with open(dior_test_json, 'r') as f:
    data = json.load(f)
    print("--------------------------------------------------")
