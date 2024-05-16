import os
import time
import usb.core


os.environ['PATH'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'libusb-1.0.24/MinGW64/dll') + os.pathsep + os.environ['PATH']


for dev in usb.core.find(find_all=True):
    try:
        speed = ['unknown', 'low', 'full', 'high', 'super'][dev.speed]

        usb_desc = f'{dev.idVendor:04X}:{dev.idProduct:04X}\n\t{dev.manufacturer}\n\t{dev.product}\n\t{speed} speed\n'

    except Exception as e:
        pass

    else:
        print(usb_desc)


while True:
    time.sleep(0.5)
