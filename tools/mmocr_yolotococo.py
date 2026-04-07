import json
import os
import shutil

import cv2

# info ，license，categories 结构初始化；
# 在train.json,val.json,test.json里面信息是一致的；





metainfo={
        "dataset_type": "train_dataset",
        "task_name": "train_task"
}
# data_list=[{
#      "img_path": "./dataset/imgs/train",
#      "height": 604,
#      "width": 640,
#      "instances":[{
#             "bbox": [0, 0, 10, 20],
#             "bbox_label": 1,
#             "mask": [0,0,0,10,10,20,20,0],
#             "text": '123'
#                   }]}]

# info，license暂时用不到
# info = {
#     "year": 2023,
#     "version": '1.0',
#     "date_created": 2023 - 8 - 13
# }

licenses={
    "id": 0,
    "name": "null",
    "url": "null",
}

# 自己的标签类别，跟yolov5的要对应好；
categories= {
    "id": 0,
    "name": 'container',
    "supercategory": 'container',
}

# 初始化train,test数据字典
# info licenses categories 在train和test里面都是一致的；
train_data = {'metainfo': metainfo, 'licenses': licenses, 'categories': categories, 'data_list': [], 'annotations': []}
test_data = {'metainfo': metainfo, 'licenses': licenses, 'categories': categories, 'data_list': [], 'annotations': []}


# image_path 对应yolov5的图像路径，比如images/train；
# label_path 对应yolov5的label路径，比如labels/train 跟images要对应；
def v5_covert_coco_format(imgs_path, label_path):
    imgs = []
    annotations = []
    for index, img_file in enumerate(os.listdir(imgs_path)):
        if img_file.endswith('.jpg'):
            imgs_info = {}
            img = cv2.imread(os.path.join(imgs_path, img_file))
            height, width, channel = img.shape
            imgs_info['id'] = index
            imgs_info['file_name'] = img_file
            imgs_info['width'], imgs_info['height'] = width, height
        else:
            continue
        if imgs_info != {}:
            imgs.append(imgs_info)
        # 处理label信息-------
        label_file = os.path.join(label_path, img_file.replace('.jpg', '.txt'))
        if os.path.exists(label_file):
            with open(label_file, 'r') as f:
                for idx, line in enumerate(f.readlines()):
                    info_annotation = {}
                    class_num, xs, ys, ws, hs = line.strip().split(' ')
                    class_id, xc, yc, w, h = int(class_num), float(xs), float(ys), float(ws), float(hs)
                    xmin = (xc - w / 2) * width
                    ymin = (yc - h / 2) * height
                    xmax = (xc + w / 2) * width
                    ymax = (yc + h / 2) * height
                    bbox_w = int(width * w)
                    bbox_h = int(height * h)
                    img_copy = img[int(ymin):int(ymax), int(xmin):int(xmax)].copy()

                    info_annotation["category_id"] = class_id  # 类别的id
                    info_annotation['bbox'] = [xmin, ymin, bbox_w, bbox_h]  ## bbox的坐标
                    info_annotation['area'] = bbox_h * bbox_w  ###area
                    info_annotation['image_id'] = index  # bbox的id
                    info_annotation['id'] = index * 100 + idx  # bbox的id
                    # cv2.imwrite(f"./temp/{info_annotation['id']}.jpg", img_copy)
                    info_annotation['segmentation'] = [[xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax]]  # 四个点的坐标
                    info_annotation['iscrowd'] = 0  # 单例
                    annotations.append(info_annotation)
    return imgs, annotations


# key == train，test，val
# 对应要生成的json文件，比如instances_train2017.json，instances_test2017.json，instances_val2017.json
# 只是为了不重复写代码。。。。。
def gen_json_file(yolov5_data_path, coco_format_path, key):
    # json path
    json_path = os.path.join(coco_format_path, f'annotations/textdet_{key}.json')
    dst_path = os.path.join(coco_format_path, f'{key}')
    if not os.path.exists(os.path.dirname(json_path)):
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
    data_path = os.path.join(yolov5_data_path, f'imgs/{key}')
    label_path = os.path.join(yolov5_data_path, f'labels/{key}')
    imgs, anns = v5_covert_coco_format(data_path, label_path)
    if key == 'train':
        train_data['imgs'] = imgs
        train_data['annotations'] = anns
        with open(json_path, 'w') as f:
            json.dump(train_data, f, indent=2)
        # shutil.copy(data_path,'')
    elif key == 'test':
        test_data['imgs'] = imgs
        test_data['annotations'] = anns
        with open(json_path, 'w') as f:
            json.dump(test_data, f, indent=2)
    else:
        print(f'key is {key}')
    print(f'generate {key} json success!')
    return


if __name__ == '__main__':
    yolov5_data_path = '/home/lixinru/Vir_env/mmocr-main/dataset'
    coco_format_path = '/home/lixinru/Vir_env/mmocr-main/dataset'
    gen_json_file(yolov5_data_path, coco_format_path, key='train')
    gen_json_file(yolov5_data_path, coco_format_path, key='test')