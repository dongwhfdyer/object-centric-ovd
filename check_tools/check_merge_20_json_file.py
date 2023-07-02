import json
from pathlib import Path

json_file = Path("datasets/DIOR_20_Merge_labled/json/0_airplane,aircraft,aeroplane_1.json")
with open(json_file, "r") as f:
    data = json.load(f)
    print("--------------------------------------------------")

