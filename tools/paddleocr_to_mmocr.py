import json
import numpy as np
import cv2
import os

# mode = 'train'
mode = 'test'
# f = open(f'/home/lixinru/Vir_env/mmocr-main/data/brand_data/brand_images/textdet_train.txt', 'r', encoding='utf-8').readlines()
f = open(f'/home/lixinru/Vir_env/mmocr-main/data/brand_data/brand_images/textdet_test.txt', 'r', encoding='utf-8').readlines()
# filename='/home/lixinru/Vir_env/mmocr-main/data/brand_data/brand_images/train/'
filename='/home/lixinru/Vir_env/mmocr-main/data/brand_data/brand_images/test/'


mmocr_label = {"metainfo": {"dataset_type": "TextDetDataset", "task_name": "textdet", "category": [{"id": 0, "name": "text"}]}, "data_list": []}
data_list = []


for line in f:
    instances = {}
    per_img_anno = []
    anno = line.split('\t')

    img_path = os.path.join(filename,anno[0])
    print((img_path))
    images_path=anno[0]

    paddle_label = anno[1]
    paddle_label = json.loads(paddle_label)

    for i in range(len(paddle_label)):
        per_box = {"polygon": [], "bbox": [], "bbox_label": 0}
        polygon = []
        points = paddle_label[i]['points']
        bounding = list(cv2.boundingRect(np.array(points)))
        if len(points) == 4:
            for j in range(len(points)):
                x, y = points[j][0], points[j][1]
                polygon.append(int(x))
                polygon.append(int(y))
                # print()
        else:
            x1, y1 = bounding[0], bounding[1]
            x2, y2 = bounding[0]+bounding[2]-1, bounding[1]
            x3, y3 = bounding[0]+bounding[2]-1, bounding[1]+bounding[3]-1
            x4, y4 = bounding[0], bounding[1]+bounding[3]-1
            polygon.append(int(x1))
            polygon.append(int(y1))
            polygon.append(int(x2))
            polygon.append(int(y2))
            polygon.append(int(x3))
            polygon.append(int(y3))
            polygon.append(int(x4))
            polygon.append(int(y4))

        bbox = [int(bounding[0]), int(bounding[1]), int(bounding[0]+bounding[2]-1), int(bounding[1]+bounding[3]-1)]

        per_box.update({"polygon": polygon})
        per_box.update({"bbox": bbox})
        per_box.update({"bbox_label": 0})
        if paddle_label[i]["transcription"] == "###":
            mark = bool(1)
            per_box.update({"ignore": mark})
        else:
            mark = bool(0)
            per_box.update({"ignore": mark})
        per_img_anno.append(per_box)
        # print()
    instances.update({"instances": per_img_anno})
    instances.update({"img_path": f'{mode}/{images_path}'})
    # instances.update({"img_path": f'{images_path}'})
    img = cv2.imread(img_path)
    instances.update({"height": img.shape[0]})
    instances.update({"weight": img.shape[1]})
    instances.update({"seg_map": f'{mode}/gt_{img_path.split(".")[0]}.txt'})
    # instances.update({"seg_map": f'gt_{img_path.split(".")[0]}.txt'})

    data_list.append(instances)

mmocr_label['data_list'] = data_list
file_name = f"textdet_{mode}.json"
# if not os.path.exists(file_name):
#     os.makedirs(file_name)
with open(f'/home/lixinru/Vir_env/mmocr-main/data/brand_data/brand_images/output/{file_name}', 'w') as f:
    str = json.dumps(mmocr_label)
    f.write(str)
    f.close()

print("close")