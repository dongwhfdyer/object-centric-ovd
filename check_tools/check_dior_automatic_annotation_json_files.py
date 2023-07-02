import json
from pathlib import Path

original_json_folder = Path("datasets/DIOR_automatic_label/json")

for json_file in original_json_folder.glob("*.json"):
    with open(json_file, "r") as f:
        data = json.load(f)
        print("--------------------------------------------------")

