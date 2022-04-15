

# 规则1：周围有两个或者三个活细胞，下一世代，该细胞仍然活着。  
# 规则2：周围少于两个活细胞，该细胞死于孤立。  
# 规则3：周围多于三个活细胞，该细胞死于拥挤。

import argparse
import numpy as np 
from enum import IntEnum
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class State(IntEnum):
    on = 255
    off = 0
def random_data(length = 4, seed = 420) -> np.array:
    '''
    生成一个大小为length的二维棋盘
    '''
    np.random.seed(seed)
    return np.random.choice([State.off, State.on], size=(length, length), p=[0.5, 0.5])

def add_bread(i, j, grid):
    bread = np.array([[0, 255, 0, 255],
                      [0, 0, 255, 255],
                      [0, 255, 0, 255],
                      [0, 255, 255, 0]])
    grid[i:i + 4, j:j + 4] = bread

def add_block(i, j, grid):
    block = np.array([[255, 255],
                     [255, 255]])
    grid[i:i + 2, j:j + 2] = block

def add_glider(i, j, grid):
    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])
    grid[i:i + 3, j:j + 3] = glider

def add_gosper_glider_gun(i, j, grid):
    gun = np.load('gosper.npy')
    grid[i:i + 11, j:j + 38] = gun

def _count(data, row, col):
    shape = data.shape[0]
    up = (row - 1) % shape
    down = (row + 1) % shape
    right = (col + 1) % shape
    left = (col - 1) % shape
    return (data[up, right] + data[up, left] +
            data[down, right] + data[down, left] +
            data[row, right] + data[row, left] +
            data[up, col] + data[down, col]) // 255

def count(initial, data, row, col):
    total = _count(initial, row, col)
    if initial[row, col]:
        if (total < 2) or (total > 3):
            data[row, col] = State.off
    else:
        if total == 3:
            data[row, col] = State.on

def update(data, save_name):
    update_interval = 50
    fig, ax = plt.subplots()
    ax.set_xticks([])
    ax.set_yticks([])
    img = ax.imshow(data, cmap='autumn', interpolation='nearest')
    ani = animation.FuncAnimation(fig, generate, fargs=(img, plt, data),
                                  frames=20,
                                  interval=update_interval,
                                  save_count=50)
    if save_name:
        ani.save(save_name, fps=30, extra_args=['-vcodec', 'libx264'])
    plt.show()

NUM = 0

def generate(frame_num, img, plt, initial):
    global NUM
    NUM += 1
    plt.title(f'{NUM} generation')
    data = initial.copy()
    rows, cols = data.shape
    for row in range(rows):
        for col in range(cols):
            count(initial, data, row, col)
    img.set_data(data)
    initial[:] = data[:]
    return img

def parse_args():
    parser = argparse.ArgumentParser(usage='生命游戏')
    parser.add_argument('--size', type=int, help='棋盘大小', required=False)
    parser.add_argument('--seed', type=int, help='随机种子', required=False)
    parser.add_argument('--glider', action='store_true', help='滑翔机', required=False)
    parser.add_argument('--gosper', action='store_true', help='高斯帕滑翔机枪', required=False)
    parser.add_argument('--save', help='文件名', required=False)
    return parser.parse_args()

def initial_data(length, seed, *, pattern=None):
    data = random_data(length, seed)
    if pattern == 'glider':
        data = np.zeros((length, length))
        add_glider(3, 3, data)
    elif pattern == 'gosper':
        data = np.zeros((length, length))
        add_gosper_glider_gun(20, 20, data)
    return data

def main():
    args = parse_args()
    length = args.size
    seed = args.seed
    glider = args.glider
    gosper = args.gosper
    save = args.save
    pattern = None
    if glider:
        pattern = 'glider'
    if gosper:
        pattern = 'gosper'
    data = initial_data(length or 50, seed or 400, pattern=pattern)
    update(data, save)

if __name__ == "__main__":
    main()



