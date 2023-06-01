from pathlib import Path

from tqdm import tqdm

#---------kkuhn-block------------------------------ # rs
folder_path = Path("datasets/MAVL_proposals/rs_props/class_specific")
folder_path2 = Path("datasets/MAVL_proposals/rs_props/class_specific2")
#---------kkuhn-block------------------------------
# #---------kkuhn-block------------------------------ # lvis
# folder_path = Path("datasets/MAVL_proposals/lvis_props/class_specific/imagenet_lvis_props")
# folder_path2 = Path("datasets/MAVL_proposals/lvis_props/class_specific/imagenet_lvis_props2")
# #---------kkuhn-block------------------------------

# if exists, delete folder2
if folder_path2.exists():
    for each_file in folder_path2.iterdir():
        each_file.unlink()
    folder_path2.rmdir()
# create folder2
folder_path2.mkdir(parents=True, exist_ok=True)

for each_folder in tqdm(folder_path.iterdir(), total=len(list(folder_path.iterdir()))):
    # create a simlink for each file in the folder
    for each_file in each_folder.iterdir():
        # create a simlink for each file in the folder
        each_file2 = folder_path2 / each_file.name
        real_path = each_file.resolve()
        each_file2.symlink_to(real_path)
