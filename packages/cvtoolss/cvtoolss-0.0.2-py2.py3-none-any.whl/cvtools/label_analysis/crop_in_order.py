# -*- coding:utf-8 -*-
# author   : gfjiangly
# time     : 2019/7/9 13:05
# e-mail   : jgf0719@foxmail.com
# software : PyCharm
import cv2
import numpy as np

import cvtools


class CropInOder(object):

    def __init__(self, width_size=1920, height_size=1080, overlap=0.):
        self.width_size = int(width_size)
        self.height_size = int(height_size)
        self.overlap = overlap

    def __call__(self, img, boxes=None, labels=None):
        h, w, c = img.shape
        crop_imgs = []
        starts = []
        # fix crop bug!
        y_stop = False
        for sy in range(0, h, int(self.height_size*(1.-self.overlap))):
            x_stop = False
            for sx in range(0, w, int(self.width_size * (1. - self.overlap))):
                ex = sx + self.width_size
                if ex > w:
                    ex = w
                    sx = w - self.width_size
                    if sx < 0:
                        sx = 0
                    x_stop = True
                ey = sy + self.height_size
                if ey > h:
                    ey = h
                    sy = h - self.height_size
                    if sy < 0:
                        sy = 0
                    y_stop = True
                # sy, ey, sx, ex = int(sy), int(ey), int(sx), int(ex)
                crop_imgs.append(img[sy:ey, sx:ex])
                starts.append((sx, sy))
                if x_stop:
                    break
            if y_stop:
                break

        if boxes is not None and labels is not None and \
                len(labels) > 0 and len(crop_imgs) > 1:
            assert len(boxes) == len(labels)
            gt_boxes = cvtools.x1y1wh_to_x1y1x2y2(boxes)
            return_imgs = []
            return_starts = []
            # return_boxes = []
            return_labels = []
            for i, crop_img in enumerate(crop_imgs):
                crop_h, crop_w, _ = crop_img.shape
                crop_x1, crop_y1 = starts[i]
                img_box = cvtools.x1y1wh_to_x1y1x2y2(np.array([[crop_x1, crop_y1, crop_w, crop_h]]))
                iof = cvtools.bbox_overlaps(gt_boxes.reshape(-1, 4), img_box.reshape(-1, 4), mode='iof').reshape(-1)
                ids = iof == 1.
                # boxes_in = boxes[ids]
                labels_in = labels[ids]
                if len(labels_in) > 0:
                    return_imgs.append(crop_img)
                    return_starts.append(starts[i])     # fix not skip start bug
                    # return_boxes.append(boxes_in)
                    return_labels.append(labels_in)
            return return_imgs, return_starts, return_labels

        return crop_imgs, starts, [labels]


if __name__ == '__main__':
    crop_in_order = CropInOder()
    img_file = 'F:/data/rssrai2019_object_detection/val/images/P0060.png'
    img = cv2.imread(img_file)
    img = crop_in_order(img)
