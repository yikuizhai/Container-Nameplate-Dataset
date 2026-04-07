import numpy as np

def calculate_IoU(poly1, poly2):
    # 将多边形的坐标格式从点列表转换为边框格式
    poly1 = [poly1[i:i+2] for i in range(0, len(poly1), 2)]
    poly2 = [poly2[i:i+2] for i in range(0, len(poly2), 2)]

    # 计算两个多边形的交集面积
    intersection = poly1_area(poly1) + poly2_area(poly2) - intersection_area(poly1, poly2)

    # 如果相交面积为0,则没有交集
    if intersection == 0:
        return 0

    # 计算两个多边形的并集面积
    union = poly1_area(poly1) + poly2_area(poly2) - intersection

    # 计算IoU
    IoU = intersection / union

    return IoU

def poly1_area(poly):
    # 计算多边形的面积
    area = 0
    n = len(poly)
    for i in range(n):
        j = (i + 1) % n
        area += poly[i][0] * poly[j][1]
        area -= poly[j][0] * poly[i][1]

    return abs(area) / 2

def poly2_area(poly):
    # 计算多边形的面积
    area = 0
    n = len(poly)
    for i in range(n):
        j = (i + 1) % n
        area += poly[i][0] * poly[j][1]
        area -= poly[j][0] * poly[i][1]

    return abs(area) / 2

def intersection_area(poly1, poly2):
    # 计算两个多边形的交集面积
    n = len(poly1)
    m = len(poly2)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        for k in range(m):
            l = (k + 1) % m
            # 计算四边形的面积
            A = (poly1[j][0] - poly1[i][0]) * (poly2[l][1] - poly2[k][1])
            B = (poly2[l][0] - poly2[k][0]) * (poly1[j][1] - poly1[i][1])
            C = (poly2[k][0] - poly1[i][0]) * (poly2[l][1] - poly2[k][1])
            D = (poly1[j][1] - poly1[i][1]) * (poly2[l][0] - poly2[k][0])

            # 如果四边形的面积大于0,则计算四边形的面积
            if abs(A + B + C + D) > 1e-10:
                area += (A + B + C + D) / 4

    return abs(area)


# # 示例输入格式
# poly2 = [0, 0, 1, 0, 1, 1, 0, 1]
# poly1 = [0, 0, 0.5, 0, 0.5, 0.5, 0, 0.5]
#
# # 计算两个多边形的IoU
# IoU = calculate_IoU(poly1, poly2)
# print("IoU:", IoU)