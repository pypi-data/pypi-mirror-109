# -*- coding: utf-8 -*-
# @Time     : 2021/6/15 17:41
# @Author   : ufy
# @Email    : antarm@outlook.com / 549147808@qq.com
# @file     : heatmap.py
# @info     :

# -*- coding: utf-8 -*-
# @Time     : 2021/6/1 10:32
# @Author   : ufy
# @Email    : antarm@outlook.com / 549147808@qq.com
# @file     :show.py
# @info     :


import seaborn as sns
from typing import Tuple
from ufy.HX.diagnosis.classify import *
from ufy.core.utils.tools import energy, find_file
from tqdm import tqdm
import os
from PIL import Image
import openslide
from matplotlib.colors import LinearSegmentedColormap


def min_max_normal(x):
    '''
    :param x: 是一个二维数据
    :return: 一个单位化的数据
    '''
    min_col = np.min(x)
    max_col = np.max(x)
    return (x - min_col + 1e-9) / (max_col - min_col + 1e-7)


def load_model(model_path):
    return joblib.load(model_path)


def load_data(tiles_fold: str, data_path: str):
    if data_path.endswith('xlsx'):
        data = pd.read_excel(data_path)
    elif data_path.endswith('csv'):
        data = pd.read_excel(data_path)
    else:
        raise ValueError('不支持该格式的数据文件')

    data = np.array(data)
    x_test = data[:, 1:885]
    x_test = np.array(x_test).astype(float)
    imgfiles = data[:, 0]
    imgfiles = tiles_fold + imgfiles
    return imgfiles, x_test


def predict(model_path, x_test):
    model = load_model(model_path)
    return model.predict_proba(x_test)[:, 1]


def grid_split(arr, grid=(1, 1)):
    out = [[None for j in range(grid[1])] for i in range(grid[0])]
    shape = arr.shape
    w_step, h_step = shape[1] // grid[1], shape[0] // grid[0]
    if shape[0] % grid[0] != 0 or shape[1] % grid[1] != 0:
        raise ValueError('Please input correct grid.')
    for i in range(grid[0]):
        for j in range(grid[1]):
            out[i][j] = arr[i * h_step:(i + 1) * h_step, j * w_step:(j + 1) * w_step]
    return np.array(out)


def grid_merge(arr):
    out = [np.hstack(arr[i, :, ...]) for i in range(arr.shape[0])]
    out = np.vstack(out)
    print('energy_matrix shape:', out.shape)
    return np.array(out)


def create_energy_matrix(imgfiles, savename, shape=(92, 44), grid=(1, 1)):
    print(grid)
    if os.path.exists(savename):
        return np.loadtxt(savename)
    energy_matrix = [[None for j in range(shape[1])] for i in range(shape[0])]
    for imgf in tqdm(imgfiles):
        img = np.array(Image.open(imgf))
        img[img == 0] = 255
        imgf = imgf.strip('.jpg')
        loc = imgf.split('_')
        i = int(loc[2]) // 2000
        j = int(loc[3]) // 2000
        energy_split = grid_split(energy(img), grid=grid)
        grid_en = [[np.mean(energy_split[i][j]) for j in range(grid[1])] for i in range(grid[0])]
        energy_matrix[i][j] = np.array(grid_en)

    print(energy_matrix)
    energy_matrix_ = np.array(energy_matrix)
    print(energy_matrix_.shape)
    out = grid_merge(energy_matrix_)
    energy_matrix_grid = min_max_normal(out)
    np.savetxt(savename, energy_matrix_grid)
    return energy_matrix_grid


def create_probablity_matrix(model_path, x_test, imgfiles, savename, shape=(92, 44), grid=(1, 1)):
    if os.path.exists(savename):
        return np.loadtxt(savename)
    model = load_model(model_path)
    y_pres = model.predict_proba(x_test)[:, 1]
    probablity_matrix = np.zeros(shape=shape)
    for i, imgf in enumerate(imgfiles):
        imgf = imgf.strip('.jpg')
        loc = imgf.split('_')
        x_loc = int(loc[2]) // 2000
        y_loc = int(loc[3]) // 2000
        probablity_matrix[x_loc][y_loc] = y_pres[i]
    image = Image.fromarray(probablity_matrix)
    image = image.resize((shape[1] * grid[1], shape[0] * grid[0]))
    probablity_matrix = np.array(image)
    np.savetxt(savename, probablity_matrix)
    return probablity_matrix


def show_img(imgfiles_dir, shape: Tuple, savename: str):
    imgs = [[None for j in range(shape[1])] for i in range(shape[0])]
    imgfiles = os.listdir(imgfiles_dir)
    for imgf in imgfiles:
        imgf_str = imgf.strip('.jpg')
        loc = imgf_str.split('_')
        x_loc = int(loc[2]) // 2000
        y_loc = int(loc[3]) // 2000
        imgs[x_loc][y_loc] = plt.imread(os.path.join(imgfiles_dir, imgf))
    for i in range(shape[0] * shape[1]):
        plt.subplot(shape[0], shape[1], i)
        plt.imread(imgs[i])
    plt.show()


def show_heatmap(heatmatrix, savename: str, cmap='rainbow'):
    sns.heatmap(heatmatrix, cmap=cmap, square=True)
    plt.savefig(savename + '_heatmap.jpg', dpi=600)
    plt.show()


def show_heatmap_img(heatmatrix, background_file, savename: str):
    plt.figure(figsize=(23, 11))
    img = plt.imread(background_file)
    fig, ax = plt.subplots()
    ax.imshow(img)
    sns.heatmap(heatmatrix, cmap='rainbow', square=True)
    plt.savefig(savename + 'heatmap_img.jpg', dpi=600)


def thumbnail(slides, savedir):
    # 保存缩略图
    for f in tqdm(slides):
        source = openslide.open_slide(f)
        img = np.array(source.read_region((0, 0), 4, source.level_dimensions[4]).convert('RGB'))
        image = Image.fromarray(img).convert(mode='RGB')
        savename1 = savedir + f.split('/')[-1].replace('.mrxs', '') + '_black.jpg'
        image.save(savename1)

        img[img == 0] = 255
        image = Image.fromarray(img).convert(mode='RGB')
        savename2 = savedir + f.split('/')[-1].replace('.mrxs', '') + '_white.jpg'
        image.save(savename2)


def main(model_path, data_path, tiles_fold, shape: Tuple, savename: str, grid: Tuple = (1, 1)):
    imgfiles, x_test = load_data(tiles_fold, data_path)  # imgfiles 存放有特征值的小瓦块的文件名
    all_tiles = find_file(dir_source=tiles_fold, file_format=['jpg'])  # all_tiles 存放所有的小瓦块的文件名
    energy_matrix_grid = create_energy_matrix(
        all_tiles, savename=savename + 'energy.txt', shape=shape, grid=grid)
    probablity_matrix_grid = create_probablity_matrix(
        model_path=model_path, x_test=x_test, imgfiles=imgfiles, savename=savename + '_probability.txt', shape=shape,
        grid=grid)

    eh_matrix = energy_matrix_grid * 0.3 + probablity_matrix_grid
    show_heatmap(min_max_normal(eh_matrix), savename=savename + '_prob_en_map.jpg')

    overlay = energy_matrix_grid * 0.3 + probablity_matrix_grid
    m = overlay.max()
    overlay[overlay < 0.01] = 2 * m

    my_colormap = LinearSegmentedColormap.from_list("normal-tumor-white", ["purple", "cyan", "yellow"])
    show_heatmap(min_max_normal(overlay), savename=savename + '_overlay_map.jpg', cmap=my_colormap)
