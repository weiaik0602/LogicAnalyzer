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
        device.write(1, msg, 100)
        attempt=0
        while True:
            ret = device.read(0x81, 3, 100)
            sret = ''.join([chr(x) for x in ret])

            #sret = bytes(sret, 'utf-8')

            sret.join('%02x' % ord(c) for c in sret)
            #sret = bytes(sret, 'utf-8')
            time=(ret[2]<<8)|ret[1]

            print(time/1000)
            data=ret[0]
            #print(data)
            #data=bytes(sret[1],'utf-8')
            #time2 = time.decode()

            #print(ret[1])
            #print(data)


            #print(sret)
            # time=(sret&0xF0)>>8
            # print(time)
            #sret=ord(sret)

            array=append(array,sret)
            attempt+=1
    #   endpoint = device[0][(0, 0)][0]
    # collected = 0
    # attempts = 50
    # while collected<attempts:
    #     try:
    #         data = device.read(endpoint.bEndpointAddress,
    #                            endpoint.wMaxPacketSize)
    #         print(data)
    #         collected+=1
    #
    #     except usb.core.USBError as e:
    #         data1 = device.read(endpoint.bEndpointAddress,
    #                            endpoint.wMaxPacketSize)
    #         data1 = None
    #         collected += 1
    #         print(data1)
    #         if e.args == ('Operation timed out',):
    #
    #             continue

if __name__ == '__main__':
  main()