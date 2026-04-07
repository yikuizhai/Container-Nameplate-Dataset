import os
import json
import cv2
import numpy as np

def calculate_bezier_control_points(rectangle):
    x, y, w, h = rectangle
    control_points = [[int(x), int(y), int(x + (w//3)), int(y), int(x + (2 * w/3)), int(y), int(x + w), int(y),
                      int(x + w ), int(y + h ), int(x + (2 * w/3)), int(y + h), int(x + (w/3)), int(y + h), int(x), int(y + h)]]

    return control_points

new_file = {"licenses": [{"url": "http://creativecommons.org/licenses/by-nc-sa/2.0/","id": 1,"name": "Attribution-NonCommercial-ShareAlike License"},
                         {"url": "http://creativecommons.org/licenses/by-nc/2.0/","id": 2,"name": "Attribution-NonCommercial License"},
                         {"url": "http://creativecommons.org/licenses/by-nc-nd/2.0/","id": 3,"name": "Attribution-NonCommercial-NoDerivs License"},
                         {"url": "http://creativecommons.org/licenses/by/2.0/","id": 4,"name": "Attribution License"},
                         {"url": "http://creativecommons.org/licenses/by-sa/2.0/","id": 5,"name": "Attribution-ShareAlike License"},
                         {"url": "http://creativecommons.org/licenses/by-nd/2.0/","id": 6,"name": "Attribution-NoDerivs License"},
                         {"url": "http://flickr.com/commons/usage/","id": 7,"name": "No known copyright restrictions"},
                         {"url": "http://www.usa.gov/copyright.shtml","id": 8,"name": "United States Government Work"}],
            "info": {"description": "COCO 2017 Dataset","url": "http://cocodataset.org","version": "1.0","year": 2017,"contributor": "COCO Consortium","date_created": "2017/09/01"},
            "categories": [{"id": 1, "name": "text", "supercategory": "beverage"}],
            "images": [],
            "annotations": []}


images = []
annos = []
CTLABELS = [' ','!','"','#','$','%','&','\'','(',')','*','+',',','-','.','/',
                             '0','1','2','3','4','5','6','7','8','9',':',';','<','=','>','?','@',
                             'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V',
                             'W','X','Y','Z','[','\\',']','^','_','`','a','b','c','d','e','f','g','h','i','j','k','l',
                             'm','n','o','p','q','r','s','t','u','v','w','x','y','z','{','|','}','~']


# file = open('/mnt/lxrnew/mingpai_dataset/train2017.txt', 'r').readlines()
file = open('/mnt/lxrnew/mingpai_dataset/val2017.txt', 'r').readlines()
count = 1
count_id = 1
s = []
for i in file:
    image = {}
    old_anno = i.split('\t')
    file_name = old_anno[0]
    id = count_id
    gt_id = count_id
    img_id = count_id

    img = cv2.imread(f'/mnt/lxrnew/mingpai_dataset/{file_name}')
    img_shape = img.shape
    while len(list(str(id))) < 4:
        id = "0" + str(id)
    file_id = str(id) + ".jpg"

    while len(list(str(gt_id))) < 7:
        gt_id = "0" + str(gt_id)

    # cv2.imwrite(f'/mnt/lxrnew/mingpai_dataset/coco/train2017/{id}.jpg', img)
    cv2.imwrite(f'/mnt/lxrnew/mingpai_dataset/coco/val2017/{id}.jpg', img)

    width, height = img_shape[1], img_shape[0]
    old_anno_set = json.loads(old_anno[1])

    for j in old_anno_set:
        anno = {}
        script = j['transcription']

        if script != '###':
            iscrowd = 0
        else:
            continue
        # list_script = list(script)
        # if len(list_script) > 25:
        #     continue
        # p = 0
        # for i in list_script:
        #     # print(i)
        #     if i not in CTLABELS:
        #         p += 1
        # if p != 0 :
        #     continue

        box = j['points']
        box_x = []
        box_y = []
        for i in box:
            box_x.append(i[0])
            box_y.append(i[1])
            min_x, max_x = min(box_x), max(box_x)
            min_y, max_y = min(box_y), max(box_y)
            w = max_x - min_x
            h = max_y - min_y
        bbox = [int(min_x), int(min_y), int(w), int(h)]
        bezier_pts = calculate_bezier_control_points(bbox)
        area = float(bbox[2] * bbox[3])
        image_id = count_id
        anno.update({"area": area, "bbox": bbox, "category_id": 1,
                     "id": count, "image_id": image_id, "iscrowd": iscrowd, "segmentation": bezier_pts})
        annos.append(anno)
        count += 1
    count_id += 1
    image.update({"coco_url": "", "date_captured": "", "file_name": file_id,
             "flickr_url": "", "id": img_id, "license": 0, "width": width, "height": height})
    images.append(image)
new_file['images'] = images
new_file['annotations'] = annos
# with open(f'/mnt/lxrnew/mingpai_dataset/coco/instances_train2017.json', 'w') as f:
with open(f'/mnt/lxrnew/mingpai_dataset/coco/instances_val2017.json', 'w') as f:
    str = json.dumps(new_file)
    f.write(str)
    f.close()



