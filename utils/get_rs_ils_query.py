import json
from pathlib import Path

id2category_json_path = Path("datasets/remote_sensing/annotations/id2category.json")

with open(id2category_json_path, "r") as f:
    rs_id2category = json.load(f)
print("--------------------------------------------------")

def get_query(cat_id):
    categories_lvis = rs_id2category
    category = categories_lvis[str(cat_id)]
    # replace _ with <space>
    category = category.replace("_", " ")
    query = f"every {category}"
    unseen = False

    return query, unseen
