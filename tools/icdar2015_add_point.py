import Polygon

for il, line in enumerate(fin):
    # line = line.strip().split(',')
    icdar_line = list(map(int, line.rstrip('\n').lstrip('\ufeff').split(',')[:8]))
    x1 = icdar_line[0] / 4 * 3 + icdar_line[2] / 4 * 1
    y1 = icdar_line[1] / 4 * 3 + icdar_line[3] / 4 * 1
    x2 = icdar_line[0] / 2 + icdar_line[2] / 2
    y2 = icdar_line[1] / 2 + icdar_line[3] / 2
    x3 = icdar_line[0] / 4 + icdar_line[2] / 4 * 3
    y3 = icdar_line[1] / 4 + icdar_line[3] / 4 * 3
    new_line = [icdar_line[0], icdar_line[1]] + [x1, y1, x2, y2, x3, y3] + [icdar_line[2], icdar_line[3]]

    x4 = icdar_line[4] / 4 * 3 + icdar_line[6] / 4
    y4 = icdar_line[5] / 4 * 3 + icdar_line[7] / 4
    x5 = icdar_line[4] / 2 + icdar_line[6] / 2
    y5 = icdar_line[5] / 2 + icdar_line[7] / 2
    x6 = icdar_line[4] / 4 + icdar_line[6] / 4 * 3
    y6 = icdar_line[5] / 4 + icdar_line[7] / 4 * 3
    text = line.rstrip('\n').lstrip('\ufeff').split(',')[8]
    new_line = new_line + [icdar_line[4], icdar_line[5]] + [x4, y4, x5, y5, x6, y6] + [icdar_line[6], icdar_line[7]]
    new_line = [int(line / math.sqrt(factor)) for line in new_line] + [text]
    line = new_line
    if not len(line[:-1]) == 20: continue
    ct = line[-1]
    if ct == '###': continue
    coords = [(float(line[:-1][ix]), float(line[:-1][ix + 1])) for ix in range(0, len(line[:-1]), 2)]
    poly = Polygon(coords)
    data.append(np.array([float(x) for x in line[:-1]]))
    cts.append(ct)
    polys.append(poly)
