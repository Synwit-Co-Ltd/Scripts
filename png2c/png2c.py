#!python3
import os
import numpy as np
import pylab as pl


def png2c(path, name):
    img = pl.imread(path) * 255
    img = img.astype(np.uint8)

    height, width, _ = img.shape

    img = img.reshape((-1, 4))

    rgb888 = [(a << 24) | (r << 16) | (g << 8) | b for (r, g, b, a) in img]

    with open(f'{name}_rgb888.h', 'w') as f:
        f.write(f'const uint32_t Image_{name}_rgb888[{height}][{width}] = {{\n')
        for i, x in enumerate(rgb888):
            if i % 16 == 0 and i != 0:
                f.write('\n')
            f.write('0x%08X, ' %x.astype(np.uint32))
        f.write('\n};')
    
    rgb565 = [(a << 16) | ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3) for (r, g, b, a) in img]
    
    with open(f'{name}_rgb565.h', 'w') as f:
        f.write(f'const uint32_t Image_{name}_rgb565[{height}][{width}] = {{\n')
        for i, x in enumerate(rgb565):
            if i % 16 == 0 and i != 0:
                f.write('\n')
            f.write('0x%06X, ' %x)
        f.write('\n};')


for name in os.listdir('.'):
    if name.endswith('.png'):
        png2c(os.path.join(os.getcwd(), name), name.split('.')[0])
