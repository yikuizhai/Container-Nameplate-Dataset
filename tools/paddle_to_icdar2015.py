import os
import json
import cv2

def ppocr_to_yolo(ppocr_label_file, image_folder, output_folder):
    with open(ppocr_label_file, 'r', encoding='utf-8') as f:
        ppocr_data = f.readlines()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for line in ppocr_data:
        line = line.strip()
        image_path, annotations = line.split('\t')
        image_width, image_height = get_image_size(os.path.join(image_folder, image_path))
        if image_width is None or image_height is None:
            continue
        image_name = os.path.basename(image_path)
        txt_path = os.path.join(output_folder, os.path.splitext(image_name)[0] + '.txt')

        with open(txt_path, 'w', encoding='utf-8') as f:
            annotations = json.loads(annotations)
            for annotation in annotations:
                transcription = annotation['transcription']
                points = annotation['points']
                difficult = annotation.get('difficult', False)

                x_min = min(points, key=lambda p: p[0])[0]
                x_max = max(points, key=lambda p: p[0])[0]
                y_min = min(points, key=lambda p: p[1])[1]
                y_max = max(points, key=lambda p: p[1])[1]
                box_width = x_max - x_min
                box_height = y_max - y_min
                center_x = (x_min + x_max) / (2 * image_width)
                center_y = (y_min + y_max) / (2 * image_height)
                box_width_normalized = box_width / image_width
                box_height_normalized = box_height / image_height

                # 使用固定的类别标签，例如类别标签为0
                class_label = 0

                line = f"{class_label} {center_x:.6f} {center_y:.6f} {box_width_normalized:.6f} {box_height_normalized:.6f}\n"
                f.write(line)
                print("done")

    print("Conversion completed.")

def ppocr_to_icdar2015(ppocr_label_file, output_folder):
    with open(ppocr_label_file, 'r', encoding='utf-8') as f:
        ppocr_data = f.readlines()

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for line in ppocr_data:
        line = line.strip()
        image_path, annotations = line.split('\t')
        image_name = os.path.basename(image_path)
        txt_path = os.path.join(output_folder, os.path.splitext(image_name)[0] + '.txt')

        with open(txt_path, 'w', encoding='utf-8') as f:
            annotations = json.loads(annotations)
            for annotation in annotations:
                transcription = annotation['transcription']
                points = annotation['points']

                x1, y1 = points[0][0], points[0][1]
                x2, y2 = points[1][0], points[1][1]
                x3, y3 = points[2][0], points[2][1]
                x4, y4 = points[3][0], points[3][1]

                line = f"{x1},{y1},{x2},{y2},{x3},{y3},{x4},{y4},{transcription}\n"
                f.write(line)

    print("Conversion completed.")


def get_image_size(image_path):
    image = cv2.imread(image_path)
    if image is not None:
        height, width, _ = image.shape
        return width, height
    else:
        return None, None

# 示例用法
ppocr_label_file = '/devdata/mingpai_dataset/brand_dataset/train_data/Label.txt'  # PPOCRLabel标注文件路径
# image_folder = 'D:\dataset\brand_images\split_brand'  # 图像文件夹路径（绝对路径）
output_folder = '/devdata/mingpai_dataset/brand_dataset/train_gt'  # 输出文件夹路径

# ppocr_to_yolo(ppocr_label_file, image_folder, output_folder)
ppocr_to_icdar2015(ppocr_label_file, output_folder)
print('done')
