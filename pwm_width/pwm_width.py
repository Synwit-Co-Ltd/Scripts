import os
import csv
from pylab import *


'''
用于观察 SimplPWM_ASYM 例程中移相后的 PWM 的占空比是否发生变化
'''


csvfile = open('DSLogic PWM.csv')
for i in range(10):
    csvfile.readline()


widths = {}
t_rise = None
t_fall = None

reader = csv.reader(csvfile)

pre_tim, _, pre_val, _ = next(reader)

for row in reader:
    tim, _, val, _ = row
    
    if pre_val == '0' and val == '1':
        t_rise = int(float(tim) * 1000000)

    elif pre_val == '1' and val == '0':
        t_fall = int(float(tim) * 1000000)

    pre_tim, pre_val = tim, val
    
    if t_rise is not None and t_fall is not None:
        widths[tim] = t_fall - t_rise

        t_rise = None
        t_fall = None


plot([float(tim) for tim in widths.keys()], widths.values())
show()
