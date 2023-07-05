import shutil
from pathlib import Path

simlink_train_test_path = Path("datasets/DIOR/train_val_test_simlinks")
if simlink_train_test_path.exists():
    shutil.rmtree(simlink_train_test_path, ignore_errors=True)
simlink_train_test_path.mkdir(parents=True, exist_ok=True)

train_path = Path("datasets/DIOR/JPEGImages-trainval")
test_path = Path("datasets/DIOR/JPEGImages-test")

for train_image in train_path.glob("*.jpg"):
    train_image_full_path = train_image.resolve()
    simlink_train_test_path.joinpath(train_image.name).symlink_to(train_image_full_path)

for test_image in test_path.glob("*.jpg"):
    test_image_full_path = test_image.resolve()
    simlink_train_test_path.joinpath(test_image.name).symlink_to(test_image_full_path)

print("done")
