import pickle

# Specify the path to the .pkl file

file_path = "/data/pcl/object-centric-ovd/datasets/MAVL_proposals/rs_20_props/class_specific/12/12_00001105.pkl"

# Open the .pkl file in read mode
with open(file_path, "rb") as f:
    # Load the contents of the .pkl file
    data = pickle.load(f)
    print("--------------------------------------------------")

# Now you can use the 'data' variable to access the loaded contents
