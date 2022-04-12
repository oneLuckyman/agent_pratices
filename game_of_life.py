

# 规则1：周围有两个或者三个活细胞，下一世代，该细胞仍然活着。  
# 规则2：周围少于两个活细胞，该细胞死于孤立。  
# 规则3：周围多于三个活细胞，该细胞死于拥挤。

import argparse
import numpy as np 
import enum
import matplotlib.pyplot as plt
from matplotlib import animation

class State(enum.IntEnum):
    on = 255
    off = 0
def random_data(length, seed) -> np.array:
    '''
    生成一个大小为length的二维棋盘
    '''
    np.random.seed(seed)
    return np.random.choice([State.off, State.on], size=(length, length), p=[0.5, 0.5])

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

def update(data, save_name = './test.html'):
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


