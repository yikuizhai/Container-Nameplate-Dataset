import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 图像文件夹路径
image_folder = '/media/newmy/data_stor/TMM_data/MSRA-TD500/train/'  # 请根据实际路径修改

# 获取图像文件列表
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg'))]
image_count = len(image_files)
print(image_count)

# 初始化总宽度、总高度和图像计数器
total_width = 0
total_height = 0
# 计算数据集中所有图像的平均宽度和高度
for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    img = cv2.imread(image_path)
    img_height, img_width, _ = img.shape
    total_width += img_width
    total_height += img_height

# 计算平均尺寸
avg_width = total_width // image_count
avg_height = total_height // image_count

# 使用平均尺寸作为统一尺寸
uniform_width = avg_width
uniform_height = avg_height

# 打印计算的平均尺寸
print(f"Average Width: {avg_width}, Average Height: {avg_height}")

# 创建一个空的总热力图
global_heatmap = np.zeros((uniform_height, uniform_width), dtype=np.float32)

# 处理每张图像并绘制热力图
for image_file in image_files:
    # 构建图像和标签的路径
    image_path = os.path.join(image_folder, image_file)
    label_path = os.path.join(image_folder, image_file.replace('JPG', 'gt'))

    # 读取图像并转换为RGB (OpenCV默认以BGR读取)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 初始化热力图
    heatmap = np.zeros((uniform_height, uniform_width), dtype=np.float32)

    # 读取标签文件并绘制边界框
    with open(label_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            x = float(parts[2])  # 边界框左上角 x 坐标
            y = float(parts[3])  # 边界框左上角 y 坐标
            w = float(parts[4])  # 边界框宽度
            h = float(parts[5])  # 边界框高度
            #
            # scale_x = uniform_width / w
            # scale_y = uniform_height / h

            # # 根据统一的尺寸缩放边界框
            # x1_pixel = int(x * scale_x)
            # y1_pixel = int(y * scale_y)
            # x2_pixel = int((x + w) * scale_x)
            # y2_pixel = int((y + h) * scale_y)

            # 根据统一的尺寸缩放边界框
            x1_pixel = int(x)
            y1_pixel = int(y)
            x2_pixel = int((x + w))
            y2_pixel = int((y + h))

            # 在热力图上绘制目标的边界框
            global_heatmap[y1_pixel:y2_pixel, x1_pixel:x2_pixel] += 1

# 应用高斯模糊，平滑热力图
global_heatmap_blurred = cv2.GaussianBlur(global_heatmap, (15, 15), 0)

# 归一化总热力图，确保值在0和1之间
global_heatmap_normalized = cv2.normalize(global_heatmap_blurred, None, 0, 1, cv2.NORM_MINMAX)

# 设置适当的图像大小以显示
print(uniform_width)
print(uniform_height)
figsize = (uniform_width / 10, uniform_height / 10)  # 用较小的比例因子
print(figsize)

# 创建图形
plt.figure(figsize=figsize)

# 显示热力图
plt.imshow(global_heatmap_normalized, cmap='hot', interpolation='nearest')
plt.axis('off')

# 保存图像到文件，确保高分辨率并且图像没有被裁剪
plt.savefig('/media/newmy/code_env/Turning/TMM/heatmap_MSRATD.jpg', bbox_inches='tight', dpi=150)
plt.close()  # 关闭图像

print("热力图已保存.")
