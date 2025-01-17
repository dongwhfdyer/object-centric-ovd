import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import torch
from detectron2.utils.events import get_event_storage
from detectron2.config import configurable
from detectron2.structures import Instances, Boxes
from detectron2.modeling.meta_arch.build import META_ARCH_REGISTRY
from detectron2.modeling.meta_arch.rcnn import GeneralizedRCNN
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
from torch.cuda.amp import autocast
import numpy as np


@META_ARCH_REGISTRY.register()
class CustomRCNNMViT(GeneralizedRCNN):
    """
    Add image labels
    """

    @configurable
    def __init__(
            self,
            with_image_labels=False,
            fp16=False,
            roi_head_name='',
            distillation=False,
            **kwargs):
        """
        """
        self.with_image_labels = with_image_labels
        self.fp16 = fp16
        self.roi_head_name = roi_head_name
        self.return_proposal = False
        super().__init__(**kwargs)
        assert self.proposal_generator is not None
        self.distillation = distillation
        self.visualized_num = 0

    @classmethod
    def from_config(cls, cfg):
        ret = super().from_config(cfg)
        ret.update({
            'with_image_labels': cfg.WITH_IMAGE_LABELS,
            'roi_head_name': cfg.MODEL.ROI_HEADS.NAME,
            'distillation': cfg.MODEL.DISTILLATION,
            'fp16': cfg.FP16,
        })
        return ret

    def inference(
            self,
            batched_inputs: Tuple[Dict[str, torch.Tensor]],
            detected_instances: Optional[List[Instances]] = None,
            do_postprocess: bool = True,
    ):
        assert not self.training
        assert detected_instances is None

        images = self.preprocess_image(batched_inputs)
        #---------kkuhn-block------------------------------ # part 1
        plt.figure()
        img_for_show = batched_inputs[0]['image'].permute(1, 2, 0).numpy()
        plt.imshow(img_for_show)
        plt.axis('off')
        # plt.show()
        #---------kkuhn-block------------------------------
        features = self.backbone(images.tensor)
        proposals, _ = self.proposal_generator(images, features, None)
        results, _ = self.roi_heads(images, (features, None), proposals)
        #---------kkuhn-block------------------------------ # part 2


        processed_res = CustomRCNNMViT._postprocess( # todo: delete this line kuhn
            results, batched_inputs, images.image_sizes)

        image_path = batched_inputs[0]['file_name']

        # pkl_path = image_path.replace('image_lable', 'pkl').replace('jpg', 'pkl')
        # with open(pkl_path, 'rb') as f:
        #     pkl = np.load(f, allow_pickle=True)
        #     for cls_id in pkl:
        #         bounding_boxes = pkl[cls_id][0]
        #         for box in bounding_boxes:
        #             x1, y1, x2, y2 = box
        #             width = x2 - x1
        #             height = y2 - y1
        #             rect = plt.Rectangle((x1, y1), width, height, fill=False, edgecolor='green')
        #             plt.gca().add_patch(rect)
        #             plt.text(x1, y1 - 5, f"Class {cls_id}", color='green')

        dior_unseen_test = Path("datasets/DIOR/Annotations/coco_split/instances_DIOR_test_unseen_2.json")
        image_id = int(image_path.split('/')[-1].split('.')[0])
        with open(dior_unseen_test, 'r') as f:
            dior_unseen_test = json.load(f)
        for ann in dior_unseen_test['annotations']:
            if int(ann['image_id']) == image_id:
                x1, y1, width, height = ann['bbox']
                rect = plt.Rectangle((x1, y1), width, height, fill=False, edgecolor='green')
                plt.gca().add_patch(rect)
                plt.text(x1, y1 - 5, f"class {ann['category_id']}", color='green')






        # Get the bounding boxes and predicted classes
        boxes = processed_res[0]['instances'].pred_boxes.tensor.cpu().numpy()
        classes = processed_res[0]['instances'].pred_classes.cpu().numpy()

        # Iterate over the bounding boxes and draw rectangles and labels
        for box, cls in zip(boxes, classes):
            x1, y1, x2, y2 = box
            width = x2 - x1
            height = y2 - y1

            # Draw the bounding box rectangle
            rect = plt.Rectangle((x1, y1), width, height, fill=False, edgecolor='red')
            plt.gca().add_patch(rect)

            # Add the predicted class label
            plt.text(x1, y1 - 5, f"Class {cls}", color='red')

        # Show the plot
        plt.axis('off')
        # plt.show()
        plt.savefig(f"output/rubb/{str(image_id)}_visualized.jpg")
        self.visualized_num += 1
        if self.visualized_num > 1000:
            exit()


        #---------kkuhn-block------------------------------

        if do_postprocess:
            assert not torch.jit.is_scripting(), \
                "Scripting is not supported for postprocess."
            return CustomRCNNMViT._postprocess(
                results, batched_inputs, images.image_sizes)
        else:
            return results

    def forward(self, batched_inputs: List[Dict[str, torch.Tensor]]):
        """
        Add ann_type
        Ignore proposal loss when training with image labels
        """
        if not self.training:
            return self.inference(batched_inputs)

        images = self.preprocess_image(batched_inputs)

        ann_type = 'box'
        gt_instances = [x["instances"].to(self.device) for x in batched_inputs]
        if self.with_image_labels:
            for inst, x in zip(gt_instances, batched_inputs):
                inst._ann_type = x['ann_type']
                inst._pos_category_ids = x['pos_category_ids']
            ann_types = [x['ann_type'] for x in batched_inputs]
            assert len(set(ann_types)) == 1
            ann_type = ann_types[0]

        if self.fp16:
            with autocast():
                features = self.backbone(images.tensor.half())
            features = {k: v.float() for k, v in features.items()}
        else:
            features = self.backbone(images.tensor)

        if ann_type == 'box':
            rpn_proposals, proposal_losses = self.proposal_generator(
                images, features, gt_instances)
        elif ann_type == 'image':

            try:
                rpn_proposals, proposal_losses = self.proposal_generator(  # 2000 proposal boxes with corresponding confidence
                    images, features, gt_instances)
            except FloatingPointError as e:
                rpn_proposals = None
                # set a large loss to prevent training
                proposal_losses = {'loss_rpn_cls': torch.tensor(1).to(self.device),
                                   'loss_rpn_loc': torch.tensor(1).to(self.device)}
                print(e)

        if (self.with_image_labels) & (ann_type == 'image'):
            proposals = self.convert_output_rpn_format_target(batched_inputs, images)  # check if the pseudo labels are loaded in dataloader
            del rpn_proposals
        else:
            proposals = rpn_proposals
        if self.distillation:
            distill_clip_features = self.get_clip_image_features(batched_inputs, images)
        else:
            distill_clip_features = None

        proposals, detector_losses = self.roi_heads(
            images, (features, distill_clip_features), proposals, gt_instances, ann_type=ann_type)

        if self.vis_period > 0:
            storage = get_event_storage()
            if storage.iter % self.vis_period == 0:
                self.visualize_training(batched_inputs, proposals)

        losses = {}
        losses.update(detector_losses)
        if self.with_image_labels:
            if ann_type == 'box':
                losses.update(proposal_losses)
            else:  # ignore proposal loss for non-bbox data
                losses.update({k: v * 0 for k, v in proposal_losses.items()})
        else:
            losses.update(proposal_losses)

        if self.return_proposal:
            return proposals, losses
        else:
            return losses

    def convert_output_rpn_format_target(self, batched_inputs, images):
        proposals: List[Instances] = []
        for n, image_size in enumerate(images.image_sizes):
            res = Instances(image_size)
            conf_thresh = 0
            if 'cls_specific_target_props' not in batched_inputs[n]:
                # preprocess here if pseudo labels not loaded in dataloader
                oredered_detections = {}
                transforms = batched_inputs[n]["transforms"]
                image_shape = batched_inputs[n]["shape"]
                key, box = batched_inputs[n]['key_bbox'][0], batched_inputs[n]['key_bbox'][1]
                box = transforms.apply_box(np.array(box))[0].clip(min=0).tolist()
                box = np.minimum(box, list(image_shape + image_shape)[::-1])
                boxes = torch.tensor(np.array([box]))
                probas = torch.tensor(np.array([1]))
                oredered_detections[key] = box, 1
                all_target_props = oredered_detections
            else:
                probas = batched_inputs[n]['cls_specific_scores']
                boxes = batched_inputs[n]['cls_specific_props']
                all_target_props = batched_inputs[n]['cls_specific_target_props']
            keep = (probas > conf_thresh)
            res.proposal_boxes = Boxes(boxes.to(images.device))
            res.objectness_logits = probas[keep]
            res.target_proposals = list(all_target_props.items())
            proposals.append(res)
        # self.debug_viz(proposals, images, 0, 0) # todo: should be commented
        return proposals

    def get_clip_image_features(self, batched_inputs, images):
        image_features = []
        region_boxes = []
        for n, image_size in enumerate(images.image_sizes):
            image_features.append(batched_inputs[n]['distill_feats'][1].to(images[n].device))
            region_boxes.append(Boxes(batched_inputs[n]['distill_feats'][0].to(images[n].device)))
        image_features = torch.cat(image_features, 0)
        return (region_boxes, image_features)

    def debug_viz(self, proposals, images, a, num=0):
        import matplotlib.pyplot as plt
        np_image = images.tensor[a].permute(1, 2, 0).detach().cpu().numpy()
        ax = plt.gca()
        xmin, ymin, xmax, ymax = proposals[a].get_fields()['proposal_boxes'].tensor[num].tolist()
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False, color="r", linewidth=5))
        plt.imshow(np_image)
        plt.show()
