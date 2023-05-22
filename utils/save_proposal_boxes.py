# ---------kkuhn-block------------------------------ # original
from external.mavl.inference.save_predictions import SavePKLFormat
import pickle
import os


class SaveProposalBoxes(SavePKLFormat):
    def __init__(self):
        super(SaveProposalBoxes, self).__init__()

    def save(self, save_path):
        for i, image_name in enumerate(self.predictions.keys()):
            with open(f"{save_path}/{image_name.split('.')[0]}.pkl", "wb") as f:
                img_to_boxes = self.predictions[image_name]
                pickle.dump(img_to_boxes, f)

    def save_imagenet(self, save_path):
        for i, image_name in enumerate(self.predictions.keys()):
            image_id = image_name.split('.')[0]
            class_id = image_id.split('_')[0]
            if not os.path.exists(f"{save_path}/{class_id}"):
                os.makedirs(f"{save_path}/{class_id}")
            with open(f"{save_path}/{class_id}/{image_id}.pkl", "wb") as f:
                img_to_boxes = self.predictions[image_name]
                pickle.dump(img_to_boxes, f)


# ---------kkuhn-block------------------------------

# # ---------kkuhn-block------------------------------ # async
#
# import asyncio
# import aiofiles
# from external.mavl.inference.save_predictions import SavePKLFormat
# import pickle
# import os
#
#
# class SaveProposalBoxes(SavePKLFormat):
#     def __init__(self):
#         super(SaveProposalBoxes, self).__init__()
#
#     async def save(self, save_path):
#         tasks = []
#         for image_name in self.predictions.keys():
#             task = asyncio.create_task(self.save_image_file(save_path, image_name))
#             tasks.append(task)
#         await asyncio.gather(*tasks)
#
#     async def save_imagenet(self, save_path):
#         tasks = []
#         for image_name in self.predictions.keys():
#             task = asyncio.create_task(self.save_image_file_imagenet(save_path, image_name))
#             tasks.append(task)
#         await asyncio.gather(*tasks)
#
#     async def save_image_file(self, save_path, image_name):
#         img_to_boxes = self.predictions[image_name]
#         async with aiofiles.open(f"{save_path}/{image_name.split('.')[0]}.pkl", "wb") as f:
#             await f.write(pickle.dumps(img_to_boxes))
#
#     async def save_image_file_imagenet(self, save_path, image_name):
#         image_id = image_name.split('.')[0]
#         class_id = image_id.split('_')[0]
#         if not os.path.exists(f"{save_path}/{class_id}"):
#             os.makedirs(f"{save_path}/{class_id}")
#         async with aiofiles.open(f"{save_path}/{class_id}/{image_id}.pkl", "wb") as f:
#             img_to_boxes = self.predictions[image_name]
#             await f.write(pickle.dumps(img_to_boxes))
# # ---------kkuhn-block------------------------------
