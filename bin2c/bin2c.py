#!python3
import os


def bin2c(path, name, prefix=''):
	with open(f'{name}.h', 'w') as f:
		f.write(f'const unsigned char {prefix}{name}[{os.stat(path).st_size}] = {{\n\t')

		for i, x in enumerate(open(path, 'rb').read()):
			if i != 0 and i % 16 == 0:
				f.write('\n\t')
			f.write(f'0x{x:02X}, ')

		f.write('\n};')


for name in os.listdir('.'):
	if name.split('.')[1] in ('bin', ):
		bin2c(os.path.join(os.getcwd(), name), name.split('.')[0])

	elif name.split('.')[1] in ('jpg', 'jpeg'):
		bin2c(os.path.join(os.getcwd(), name), name.split('.')[0], 'jpeg_')
