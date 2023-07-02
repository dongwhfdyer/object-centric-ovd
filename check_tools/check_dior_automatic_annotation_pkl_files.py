import json
import pickle
from pathlib import Path

pkl_folder = Path("datasets/DIOR_automatic_label/pkl")

for pkl_file in pkl_folder.glob("*.pkl"):
    with open(pkl_file, "rb") as f:
        data =  pickle.load(f)
        print("--------------------------------------------------")
