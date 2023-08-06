# -*- encoding:utf-8 -*-
# @Time    : 2019/6/19 19:35
# @Author  : gfjiang
# @Site    : 
# @File    : rscup_to_coco.py
# @Software: PyCharm
import json
import os
from tqdm import tqdm
import cv2.cv2 as cv
from PIL import Image
import numpy as np

import cvtools


class Rscup2COCO(object):
    def __init__(self,
                 label_root,
                 image_root,
                 cls_map='rscup/cat_id_map.txt',
                 path_replace=None,
                 box_form='x1y1wh'):
        self.label_root = label_root
        self.image_root = image_root
        self.path_replace = path_replace
        self.box_form = box_form
        self.files = cvtools.get_files_list(label_root, basename=True)
        self.lines = []
        self.cls_map = cvtools.read_key_value(cls_map)
        self.coco_dataset = {
            "info": {
                "description": "This is stable 1.0 version of the 2019 rscup race.",
                "url": "http://rscup.bjxintong.com.cn/#/theme/2",
                "version": "1.0", "year": 2019,
                "contributor": "rscup",
                "date_created": cvtools.get_now_time_str()
            },
            "categories": [],
            "images": [], "annotations": []
        }
        self.imageID = 1
        self.annID = 1
        self.run_timer = cvtools.Timer()

    def convert(self, use_crop=False):
        for key, value in self.cls_map.items():
            self.coco_dataset['categories'].append({
                'id': int(value),
                'name': key,
                'supercategory': key
            })
        for file in tqdm(self.files):
            with open(os.path.join(self.label_root, file), 'r') as f:
                lines = f.readlines()
            # !only do once for one file label
            image_name = file.replace('.txt', '.png')
            if use_crop:
                image_name = file.split('_')[0] + '.png'
            image_file = os.path.join(self.image_root, image_name)
            try:
                # self.run_timer.tic()
                "PIL: Open an image file, without loading the raster data"
                im = Image.open(image_file)
                # im = cv2.imdecode(np.fromfile(image_name, dtype=np.uint8), cv2.IMREAD_COLOR)
                # self.run_timer.toc(average=False)
                if im is None:
                    print('Waring: !!!can\'t read %s, continue this image' % image_file)
                    continue
                # height, width, _ = im.shape
                width, height = im.size
            except (FileNotFoundError, Image.DecompressionBombError) as e:
                print(e)
                continue

            # add image information to dataset
            for key, value in self.path_replace.items():
                image_name = image_name.replace(key, value)
            img_info = {
                'file_name': image_name,    # relative path
                'id': self.imageID,
                'width': width,
                'height': height,
            }
            if use_crop:
                crop = list(map(int, os.path.basename(file).split('.')[0].split('_')[2:]))
                img_info['width'] = crop[2] - crop[0]
                img_info['height'] = crop[3] - crop[1]
                img_info['crop'] = crop
            self.coco_dataset["images"].append(img_info)

            ignore = 0
            if height * width > 100000000:
                ignore = 1

            for line in lines:
                line = line.strip().split()
                if len(line) != 10:
                    continue
                polygon = list(map(float, [item.strip() for item in line[:8]]))
                a = np.array(polygon).reshape(4, 2)  # prepare for Polygon class input
                a_hull = cv.convexHull(a.astype(np.float32), clockwise=False)  # 顺时针输出凸包

                if self.box_form == 'x1y1wh':
                    box = cv.boundingRect(a_hull)
                    area = box[2] * box[3]
                elif self.box_form == 'xywha':
                    xywha = cv.minAreaRect(a_hull)
                    area = xywha[1][0] * xywha[1][1]
                    box = list(xywha[0]) + list(xywha[1]) + [xywha[2]]
                elif self.box_form == 'x1y1x2y2x3y3x4y4':
                    area = cv.contourArea(a_hull)
                    box = list(a_hull.reshape(-1).astype(np.float))
                else:
                    raise TypeError("not support {} box format!".format(self.box_form))

                box = list(map(lambda x: round(x, 2), box))
                cat = line[8].strip()
                difficult = int(line[9].strip())
                self.coco_dataset['annotations'].append({
                    'area': area,
                    'bbox': box,
                    'category_id': int(self.cls_map[cat]),  # 0 for backgroud
                    'id': self.annID,
                    'image_id': self.imageID,
                    'iscrowd': 0,
                    'ignore': ignore,
                    'difficult': difficult,
                    'segmentation': [polygon]
                })
                self.annID += 1
            self.imageID += 1

    def save_json(self, to_file='cocolike.json'):
        # save json format results to disk
        cvtools.utils.makedirs(to_file)
        with open(to_file, 'w') as f:
            json.dump(self.coco_dataset, f)  # using indent=4 show more friendly
        print('!save {} finished'.format(to_file))


if __name__ == '__main__':
    label_root = 'D:/data/rssrai2019_object_detection/train/labelTxt/'
    crop_label_root = '../label_analysis/rscup/crop800x800/train/labelTxt+crop'
    image_root = 'D:/data/rssrai2019_object_detection/train/images/'
    path_replace = {'\\': '/'}
    rscup_to_coco = Rscup2COCO(crop_label_root, image_root, path_replace=path_replace, box_form='x1y1wh')
    rscup_to_coco.convert(use_crop=True)
    rscup_to_coco.save_json('rscup/crop800x800_train_rscup_x1y1wh_polygen.json')
