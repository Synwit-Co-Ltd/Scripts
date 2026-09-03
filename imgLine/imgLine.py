from PIL import Image
from pylab import *


'''	生成一张图片的像素数据，大小 128*128，颜色为白色，左侧有一条红色的竖线
'''


rgb888 = [[(0xFF, 0xFF, 0xFF) for j in range(128)] for i in range(128)]

for i in range(128):
	rgb888[i][2] = (0xFF, 0x00, 0x00)

imshow(rgb888)
show()


def rgb888to565(pixel):
	r, g, b = pixel
	r = r >> 3
	g = g >> 2
	b = b >> 3

	return (r << 11) | (g << 5) | b


rgb565 = [[rgb888to565(pixel) for pixel in row] for row in rgb888]
rgb565 = array(rgb565).reshape(-1)

name, height , width = 'imgLine', 128, 128

with open(f'{name}_rgb565.h', 'w') as f:
    f.write(f'const uint16_t {name}_rgb565[{height}][{width}] = {{\n')
    for i, x in enumerate(rgb565):
        if i % 16 == 0 and i != 0:
            f.write('\n')
        f.write('0x%04X, ' %x)
    f.write('\n};')
