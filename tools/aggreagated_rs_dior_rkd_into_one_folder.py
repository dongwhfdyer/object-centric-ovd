# import os
# import sys
# from pathlib import Path
#
# # Define the paths of the source folders and the target folder
# src_folder1 = "datasets/MAVL_proposals/rs_props/classagnostic_distilfeats"
# src_folder2 = "datasets/MAVL_proposals/dior_props/classagnostic_distilfeats"
# target_folder = "datasets/MAVL_proposals/rs_dior_aggregated"
#
# # Create the target folder if it does not exist
# Path(target_folder).mkdir(parents=True, exist_ok=True)
#
#
# def create_symlinks(src_folder: str) -> None:
#     for subdir, _, files in os.walk(src_folder):
#         for file in files:
#             # Check if the file ends with .pkl extension
#             if file.endswith(".pkl"):
#                 src_file_path = os.path.join(subdir, file)
#                 target_file_path = os.path.join(target_folder, file)
#
#                 # Avoid overwriting existing symlink
#                 if not os.path.exists(target_file_path):
#                     # Create a symbolic link in the target folder
#                     try:
#                         os.symlink(src_file_path, target_file_path)
#                     except OSError as e:
#                         sys.stderr.write(f"Error creating symlink: {e}\n")
#                 else:
#                     sys.stderr.write(f"Skipping existing symlink for: {file}\n")
#
#
# # Create symlinks for both source folders
# create_symlinks(src_folder1)
# create_symlinks(src_folder2)
#
# import os
# import sys
# import shutil
# from pathlib import Path
#
# # Define the paths of the source folders and the target folder
# src_folder1 = "datasets/MAVL_proposals/rs_props/classagnostic_distilfeats"
# src_folder2 = "datasets/MAVL_proposals/dior_props/classagnostic_distilfeats"
# target_folder = "datasets/MAVL_proposals/rs_dior_aggregated"
#
# # Remove the target folder if it exists, then create a new one
# if os.path.exists(target_folder):
#     shutil.rmtree(target_folder)
# Path(target_folder).mkdir(parents=True, exist_ok=True)
#
#
# def create_symlinks(src_folder: str) -> None:
#     for subdir, _, files in os.walk(src_folder):
#         for file in files:
#             # Check if the file ends with .pkl extension
#             if file.endswith(".pkl"):
#                 src_file_path = os.path.abspath(os.path.join(subdir, file))
#                 target_file_path = os.path.join(target_folder, file)
#
#                 # Avoid overwriting existing symlink
#                 if not os.path.exists(target_file_path):
#                     # Create a symbolic link in the target folder
#                     try:
#                         os.symlink(src_file_path, target_file_path)
#                     except OSError as e:
#                         sys.stderr.write(f"Error creating symlink: {e}\n")
#                 else:
#                     sys.stderr.write(f"Skipping existing symlink for: {file}\n")
#
#
# # Create symlinks for both source folders
# create_symlinks(src_folder1)
# create_symlinks(src_folder2)

import os
import sys
import shutil
from pathlib import Path
from tqdm import tqdm

# Define the paths of the source folders and the target folder
src_folder1 = "datasets/MAVL_proposals/rs_props/classagnostic_distilfeats"
src_folder2 = "datasets/MAVL_proposals/dior_props/classagnostic_distilfeats"
target_folder = "datasets/MAVL_proposals/rs_dior_aggregated"

# Remove the target folder if it exists, then create a new one
if os.path.exists(target_folder):
    shutil.rmtree(target_folder)
Path(target_folder).mkdir(parents=True, exist_ok=True)

def create_symlinks(src_folder: str) -> None:
    # Get the total number of files for the progress bar
    total_files = sum([len(files) for _, _, files in os.walk(src_folder)])

    with tqdm(total=total_files, desc="Creating symlinks") as pbar:
        for subdir, _, files in os.walk(src_folder):
            for file in files:
                pbar.update(1)  # Update the progress bar

                # Check if the file ends with .pkl extension
                if file.endswith(".pkl"):
                    src_file_path = os.path.abspath(os.path.join(subdir, file))
                    target_file_path = os.path.join(target_folder, file)

                    # Avoid overwriting existing symlink
                    if not os.path.exists(target_file_path):
                        # Create a symbolic link in the target folder
                        os.symlink(src_file_path, target_file_path)
                    else:
                        print(target_file_path)

# Create symlinks for both source folders
create_symlinks(src_folder1)
create_symlinks(src_folder2)
