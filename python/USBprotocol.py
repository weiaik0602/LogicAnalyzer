import numpy as np
import usb.core
import usb.util
import usb.backend.libusb0 as libusb0
#define USB backend
from ctypes import*
backend = usb.backend.libusb0.get_backend(find_library=lambda x: "C:\\WINDOWS\\system32\\libusb-1.0.dll")

#MY Define
OPERATION_SETPORT = 0xC
DIGITAL = 0
ANALOG  = 0
#MY Function

def PortCompressFunc(type,array):
    DPArray=0
    APArray=0

    if type==DIGITAL :
        for x in array:
            DPArray=(DPArray)|(1<<x)
        return DPArray
    if type==ANALOG :
        for x in array:
            APArray=(APArray)|(1<<x)
        return APArray

def getUpperByte(x):
    return (x & 0xFF00)>>8
def getLowerByte(x):
    return (x&0xFF)

print("Welcome to XXX\n")

print("Finding USB device")
#find device(STM32 CDC device)	idVendor=0x0483, idProduct=0x5740
device=usb.core.find(idVendor=0x0483, idProduct=0x5740,backend=backend)
if device is None:
    raise ValueError('No device found. Please connect the device and try again')
else:
    print("Device is found")
    device.set_configuration()


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
        print(type(AP))
        print("value stored!!!")
    # if not come out from the loop
    except:
        print("all the port taken")
        break
    NumofAP.append(int(AP))


TotalNumofAP=len(NumofAP)



DPArray=PortCompressFunc(DIGITAL,NumofDP)
APArray=PortCompressFunc(ANALOG,NumofAP)
configuration=bytes([OPERATION_SETPORT,4,getUpperByte(DPArray),getLowerByte(DPArray),getUpperByte(APArray),getLowerByte(APArray)])
print(list(configuration))

device.write(1, configuration, 200)
while True:
    ret = device.read(0x81, 23, 520)
    print(list(ret))