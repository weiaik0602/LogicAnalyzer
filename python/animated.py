from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import usb.core
import usb.util
import usb.backend.libusb0 as libusb0
#define USB backend
from ctypes import*
backend = usb.backend.libusb0.get_backend(find_library=lambda x: "C:\\WINDOWS\\system32\\libusb-1.0.dll")

#MY Define
OPERATION_SETPORT = 0x22
DIGITAL = 0
ANALOG  = 0xF
#MY Function

def PortCompressFunc(type,array):
    DPArray=0
    APArray=0

    if type==DIGITAL :
        for x in array:
            DPArray=(DPArray)|(1<<x)
        return DPArray|(DIGITAL<<12)
    if type==ANALOG :
        for x in array:
            APArray=(APArray)|(1<<x)
        return APArray|(ANALOG<<12)

def getUpperByte(x):
    return (x & 0xFF00)>>8
def getLowerByte(x):
    return (x&0xFF)

print("Welcome to XXX\n")

print("Finding USB device")
#find device(STM32 CDC device)	idVendor=0x0483, idProduct=0x5740
device=usb.core.find(idVendor=0x0483, idProduct=0x5740,backend=backend)
# if device is None:
#     raise ValueError('No device found. Please connect the device and try again')
# else:
#     print("Device is found")
#     device.set_configuration()


print("Key in the DP port you wish to use(0~9)")
NumofDP = []
while True:
    DP = (input())
    try:
        DP = float(DP)
        DP = int(DP)
        print("value stored!!!")
    # if not come out from the loop
    except:
        print("all the port taken")
        break
    NumofDP.append(int(DP))

TotalNumofDP=len(NumofDP)

print("Key in the AP port you wish to use(0~9)")
NumofAP=[]
while True:
    AP = input()
    try:
        AP = float(AP)
        AP = int(AP)
        print("value stored!!!")
    # if not come out from the loop
    except:
        print("all the port taken")
        break
    NumofAP.append(int(AP))


TotalNumofAP = len(NumofAP)


DPArray=PortCompressFunc(DIGITAL,NumofDP)
APArray=PortCompressFunc(ANALOG,NumofAP)
configuration=bytes([OPERATION_SETPORT,getUpperByte(DPArray),getLowerByte(DPArray),getUpperByte(APArray),getLowerByte(APArray)])
print(list(configuration))

#device.write(1, configuration, 100)


#take value configured and plot graph
# Sent for figure
font = {'size': 9}
matplotlib.rc('font', **font)

# Setup figure and subplots
f0=plt.figure(figsize = (15, 15))#)

#f0 = figure(num = 0, figsize = (12, 8))#, dpi = 100)
f0.suptitle("Logic Analyzer", fontsize=12)

#plot subplot
DPArray = list()
APArray = list()
DPSubplot = dict()
APSubplot = dict()
odd = 1
even = 2
for i , num in enumerate( NumofDP , 0):
    #append the str DP and te number
    DPArray.append(f"DP{str(num)}")
    if odd==1:
        DPSubplot[DPArray[i]]=plt.subplot(TotalNumofDP,2,odd)
    else:
        DPSubplot[DPArray[i]] = plt.subplot(TotalNumofDP, 2, odd,sharex=DPSubplot[DPArray[0]])
        plt.setp(DPSubplot[DPArray[i-1]].get_xticklabels(), visible = False)
    DPSubplot[DPArray[i]].set_ylim(0,5)
    DPSubplot[DPArray[i]].set_xlim(0,10)
    DPSubplot[DPArray[i]].set_ylabel(DPArray[i],rotation=0)

    odd+=2

for i , num in enumerate( NumofAP , 0):
    #append the str AP and te number
    APArray.append(f"AP{str(num)}")
    if even==2:
        APSubplot[APArray[i]]=plt.subplot(TotalNumofAP,2,even)
    else:
        APSubplot[APArray[i]] = plt.subplot(TotalNumofAP, 2, even,sharex=APSubplot[APArray[0]])
        plt.setp(APSubplot[APArray[i-1]].get_xticklabels(), visible = False)
    APSubplot[APArray[i]].set_ylim(0,5)
    APSubplot[APArray[i]].set_xlim(0,10)
    APSubplot[APArray[i]].set_ylabel(APArray[i],rotation=0)
    even+=2


#set to full screen
manager = plt.get_current_fig_manager()
manager.window.state('zoomed')



#simulation = animation.FuncAnimation(f0, updateData, blit=False, frames=None, interval=1, repeat=False)

plt.show()