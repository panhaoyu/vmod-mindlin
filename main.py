import os
import shutil
import numpy as np
import parse_head
import stiffness
import matplotlib.pyplot as plt
from functools import reduce

# 配置文件路径
project = 'expand3'
run = 'Run20'
src = f'C:\\Users\\wolf\\Desktop\\Shang Shi Center\\{project}.data\\MODFLOW\\' \
    f'NumericalGrid_refined_refined\\{run}\\MODFLOW-2005\\Wall depth.LST'

name = 'initial_head_80_connect_-10'

dst = os.path.join(f'D:\\OneDrive\\大四下学期\\毕业设计\\vmod\\lst', f'{name}.txt')
shutil.copy(src, dst)

# 设置网格的宽高
border_length = [50] * 7 + [10] * 30 + [50] * 7
border_width = [50] * 7 + [10] * 30 + [50] * 7

# 设置初始水头
initial_head = 80

# 设置基坑的位置
foundation_position = (slice(15, 29), slice(15, 29))

# 设置监测点的位置
monitoring_point_140_140 = (
    # 传参为displacement[23]行向量
    lambda d: d[30] * 1 / 2 + d[31] * 1 / 2,
    lambda d: d[32] * 1 / 2 + d[33] * 1 / 2,
    lambda d: d[37] * 1 / 6 + d[38] * 5 / 6,
    lambda d: d[39] * 1 / 10 + d[40] * 9 / 10,
)

monitoring_point = (
    lambda d: d[28] * 1 / 2 + d[29] * 1 / 2,
    lambda d: d[35] * 1 / 2 + d[36] * 1 / 2,
    lambda d: d[37] * 5 / 6 + d[38] * 1 / 6,
    lambda d: d[39] * 1 / 2 + d[40] * 1 / 2,
)

# 转换网格的宽高为numpy格式
border_length = np.asarray(border_length)
border_width = np.asarray(border_width)
mesh_length = np.tile(border_length, (len(border_width), 1))
mesh_width = np.tile(border_width, (len(border_length), 1)).T

# 计算网格的矩阵形状
shape = (len(border_length), len(border_width))

# 计算网格的格点的坐标
border_corner_x = reduce(lambda a, b: np.append(a, b + a[-1]), border_length, np.zeros((1,)))
border_corner_y = reduce(lambda a, b: np.append(a, b + a[-1]), border_width, np.zeros((1,)))

# 计算网格的中点的坐标
border_center_x = (border_corner_x[:-1] + border_corner_x[1:]) / 2
border_center_y = (border_corner_y[:-1] + border_corner_y[1:]) / 2
mesh_center = np.asarray([(x, y) for x in border_center_x for y in border_center_y]).reshape((*shape, 2))
mesh_center_x = mesh_center[:, :, 0]
mesh_center_y = mesh_center[:, :, 1]

# 获取水头信息
head = parse_head.get_heads(dst).reshape(shape)

# 计算水头降深
head_diff = np.ones(shape, np.float_) * initial_head - head

# 忽略基坑内的水位降低引起的反力
head_diff[foundation_position] = 0

# 计算网格的合力作为集中力
force = head_diff * 9.8E3 * mesh_width * mesh_length

# 计算刚度矩阵
stiffness_matrix = stiffness.generate_mindlin_stiffness_matrix(
    x_list=mesh_center[:, :, 0],
    y_list=mesh_center[:, :, 1],
    depth=initial_head
)

stiffness_matrix_same_position = [stiffness_matrix[i, i] for i in range(44 * 44)]
stiffness_matrix_same_position = np.asarray(stiffness_matrix_same_position).reshape(shape)

# 计算各网格中心处的位移
displacement = np.dot(stiffness_matrix, force.reshape(44 * 44)).reshape(shape)


def plot(matrix, path):
    C = plt.contour(border_center_x, border_center_y, matrix, 20, colors='black')
    plt.contourf(border_center_x, border_center_y, matrix, 100)
    plt.clabel(C, inline=1, fontsize=10)
    plt.savefig(path)
    plt.close()
    return plt


# 输出水头图和沉降图
figure_path_displacement = os.path.join(r'D:\OneDrive\大四下学期\毕业设计\vmod\picture', f'{name}_displacement.jpg')
figure_path_head = os.path.join(r'D:\OneDrive\大四下学期\毕业设计\vmod\picture', f'{name}_head.jpg')
plot(displacement, figure_path_displacement)
plot(head_diff, figure_path_head)

# 输出监测点处的沉降
path_monitoring_point = os.path.join(r'D:\OneDrive\大四下学期\毕业设计\vmod\monitoring_point', f'{name}.txt')
with open(path_monitoring_point, mode='a', encoding='utf-8') as file:
    for i, point in enumerate(monitoring_point):
        file.write(f'{i}\t{point(displacement[23])}\n')

pass
