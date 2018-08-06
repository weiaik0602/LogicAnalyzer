import usb.core
import usb.util
import usb.backend.libusb0 as libusb0
import numpy
import datetime
from datetime import datetime, date

from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot

from ctypes import*
# give location of dll
backend = usb.backend.libusb0.get_backend(find_library=lambda x: "C:\\WINDOWS\\system32\\libusb-1.0.dll")

from struct import *
def main():
    array=zeros(0)
    device=usb.core.find(idVendor=0x0483, idProduct=0x5740,backend=backend)


    if device is None:
        print('Not found')
    else:
        print('Found')
        #print(device)
        device.set_configuration()
        msg = 'test'
        device.write(1, msg, 150)
        attempt=0
        while True:
            ret = device.read(0x81, 30, 510)
            time=((ret[0]<<8)|ret[1])/2
            data = ret[2]
            print(ret)

            attempt+=1

if __name__ == '__main__':
  main()