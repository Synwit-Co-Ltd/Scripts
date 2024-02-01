#!python3
import os
import pylab as pl


def jpeg2c(path, name):
    img = pl.imread(path)

    height, width, _ = img.shape

    img = img.reshape((-1, 3))

    rgb888 = [(r << 16) | (g << 8) | b for (r, g, b) in img]

    with open(f'{name}_rgb888.h', 'w') as f:
        f.write(f'const uint32_t Image_{name}_rgb888[{height}][{width}] = {{\n')
        for i, x in enumerate(rgb888):
            if i % 16 == 0 and i != 0:
                f.write('\n')
            f.write('0x%06X, ' %x)
        f.write('\n};')

    rgb565 = [((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3) for (r, g, b) in img]
    
    with open(f'{name}_rgb565.h', 'w') as f:
        f.write(f'const uint16_t Image_{name}_rgb565[{height}][{width}] = {{\n')
        for i, x in enumerate(rgb565):
            if i % 16 == 0 and i != 0:
                f.write('\n')
            f.write('0x%04X, ' %x)
        f.write('\n};')


for name in os.listdir('.'):
    if name.endswith('.jpg') or name.endswith('.jpeg'):
        jpeg2c(os.path.join(os.getcwd(), name), name.split('.')[0])
