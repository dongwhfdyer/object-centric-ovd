import numpy as np
from torch.nn import functional as F
from detectron2.config import configurable
from detectron2.layers import ShapeSpec
from detectron2.modeling.roi_heads.roi_heads import ROI_HEADS_REGISTRY, Res5ROIHeads
from .custom_fast_rcnn import CustomFastRCNNOutputLayers


@ROI_HEADS_REGISTRY.register()
class CustomRes5ROIHeads(Res5ROIHeads):
    @configurable
    def __init__(self, **kwargs):
        cfg = kwargs.pop('cfg')
        super().__init__(**kwargs)
        stage_channel_factor = 2 ** 3
        out_channels = cfg.MODEL.RESNETS.RES2_OUT_CHANNELS * stage_channel_factor

        self.with_image_labels = cfg.WITH_IMAGE_LABELS
        self.ws_num_props = cfg.MODEL.ROI_BOX_HEAD.WS_NUM_PROPS
        self.box_predictor = CustomFastRCNNOutputLayers(
            cfg, ShapeSpec(channels=out_channels, height=1, width=1)
        )
        self.visualize_num = 0  # todo: only for visualization index

    @classmethod
    def from_config(cls, cfg, input_shape):
        ret = super().from_config(cfg, input_shape)
        ret['cfg'] = cfg
        return ret

    def forward(self, images, features, proposals, targets=None, ann_type='box'):
        # # ---------kkuhn-block------------------------------ # todo: if you want to use the original version, please uncomment.
        # del images
        # # ---------kkuhn-block------------------------------

        features, distill_clip_features = features
        if self.training:
            if ann_type == 'box':
                proposals = self.label_and_sample_proposals(proposals, targets)
            else:
                proposals = self.get_top_proposals(proposals)  # proposals_ = self.get_top_proposals(proposals)
        # ---------kkuhn-block------------------------------ # todo: comment kuhn: uncomment only for visualization of the proposals
        import matplotlib.pyplot as plt

        top_proposals = self.get_top_proposals(proposals, 30)
        image_size = images.image_sizes[0]
        image_tensor = images.tensor[0].cpu().numpy().astype(int)
        # the image are soo dark, so we need to do histogram equalization
        image_tensor = image_tensor - image_tensor.min()
        image_tensor = image_tensor / image_tensor.max()
        image_tensor = (image_tensor * 255).astype(int)
        # convert to rgb
        image_tensor_ = image_tensor[::-1, :, :]

        # use split to get the seperate color channels
        # image_tensor = np.split(image_tensor, 3, axis=2)

        # Create the figure and axes
        fig, ax = plt.subplots(figsize=(10, 10))

        # Display the image on the created axes
        ax.imshow(image_tensor_.transpose(1, 2, 0))

        # close the axis
        ax.axis('off')

        top_proposals_ = top_proposals[0].proposal_boxes.tensor
        for proposal in top_proposals_:
            x1, y1, x2, y2 = proposal.cpu().numpy().astype(int).tolist()
            width = x2 - x1
            height = y2 - y1
            rect = plt.Rectangle((x1, y1), width, height, fill=False, color='red')
            ax.add_patch(rect)

        # plt.show()
        plt.savefig('rubb/visualized/{}.png'.format(self.visualize_num), bbox_inches='tight', pad_inches=0)

        self.visualize_num += 1

        # ---------kkuhn-block------------------------------
        proposal_boxes = [x.proposal_boxes for x in proposals]
        box_features = self._shared_roi_transform([features[f] for f in self.in_features], proposal_boxes)
        predictions = self.box_predictor(box_features.mean(dim=[2, 3]))

        if self.training and distill_clip_features is not None:
            # distilling image embedding
            distil_regions, distill_clip_embeds = distill_clip_features
            region_level_features = self._shared_roi_transform([features[f] for f in self.in_features], distil_regions)
            image_embeds = region_level_features.mean(dim=[2, 3])
            # image distillation
            proj_image_embeds = self.box_predictor.cls_score.linear(image_embeds)
            norm_image_embeds = F.normalize(proj_image_embeds, p=2, dim=1)
            normalized_clip_embeds = F.normalize(distill_clip_embeds, p=2, dim=1)
            distill_features = (norm_image_embeds, normalized_clip_embeds)
        else:
            distill_features = None

        if self.training:
            del features
            if ann_type != 'box':
                image_labels = [x._pos_category_ids for x in targets]
                losses = self.box_predictor.image_label_losses(
                    predictions, proposals, distill_features, image_labels)
            else:
                losses = self.box_predictor.losses(
                    (predictions[0], predictions[1]), proposals, distill_features)
                if self.with_image_labels:
                    assert 'pms_loss' not in losses
                    losses['pms_loss'] = predictions[0].new_zeros([1])[0]
            return proposals, losses
        else:
            pred_instances, _ = self.box_predictor.inference(predictions, proposals)
            pred_instances = self.forward_with_given_boxes(features, pred_instances)
            return pred_instances, {}

    def get_top_proposals(self, proposals, num_props=128):
        for i in range(len(proposals)):
            proposals[i].proposal_boxes.clip(proposals[i].image_size)
        proposals = [p[:num_props] for p in proposals]
        return proposals
