from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import usb.core
import usb.util
import usb.backend.libusb0 as libusb0
from ctypes import *
from array import *


# MY Define
STATE_CONFIG = 0xc
STATE_SEND_DP = 0xa
STATE_SEND_AP = 0xb
DIGITAL = 0
ANALOG = 1
xmax = 10.0
#Global variable
timeDiff = 0
APData = []
DPData = []
DPArray = list()
APArray = list()
DPPlotsArray = list()
APPlotsArray = list()
dataDP = dict()
dataAP = dict()
time = zeros(0)
TotalNumofDP=0
TotalNumofAP=0
DPSubplot = dict()
APSubplot = dict()
device = None
dataAPArray=[[0 for x in range(1)] for y in range(5)]
dataDPArray=[[0 for x in range(1)] for y in range(5)]
#Function
def findUSBNConfig():
    print("Finding USB device")
    # define USB backend
    backend = usb.backend.libusb0.get_backend(find_library=lambda x: "C:\\WINDOWS\\system32\\libusb-1.0.dll")
    # find device(STM32 CDC device)	idVendor=0x0483, idProduct=0x5740
    device = usb.core.find(idVendor=0x0483, idProduct=0x5740, backend=backend)
    if device is None:
        raise ValueError('No device found. Please connect the device and try again')
    else:
        print("Device is found")
        device.set_configuration()
    return device
def keyInDP():
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
    return NumofDP
def keyInAP():
    print("Key in the AP port you wish to use(0~9)")
    NumofAP = []
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
    return NumofAP
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
def breakTimeData(value=[]):
    global timeDiff
    timeDiff=0
    n=-1
    while True:
        if ((value[n]) >>7)==1 :
            timeDiff = ((value[n] & 0x7F) | timeDiff << (7))
            n -= 1
        else:
            timeDiff = ((value[n] & 0x7F) | timeDiff << 7)
            n-=1
            break
    return (n)
def breakDataForAP(USBData=[]):
    global APData
    APData[:]=[]
    dataCounter=breakTimeData(USBData)
    evencounter=0
    oddcounter=1
    counter=0
    max=len(USBData)+dataCounter
    while (counter*2)<=(max):
        APData.insert(counter,USBData[oddcounter]<<8|USBData[evencounter])
        counter+=1
        evencounter += 2
        oddcounter += 2
def breakDataForDP(USBData=[]):
    global DPData
    DPData[:]=[]
    DPtemp=0
    dataCounter = breakTimeData(USBData)
    counter = 0
    max = len(USBData) + dataCounter
    if USBData[dataCounter]==USBData[0]:
        DPtemp = USBData[0]
    else :
        DPtemp=USBData[dataCounter]<<8|USBData[0]
    while DPtemp:
        DPData.insert(counter,DPtemp&0x01)
        counter+=1
        DPtemp>>=1
def receiveData(ret=[]):
    if ret[-1]==STATE_SEND_DP:
        breakDataForDP(ret)
    if ret[-1] == STATE_SEND_AP:
        breakDataForAP(ret)
def setAPPlots(dataAP=[],APSubplots=[]):
    global time
    APPlotsArray = dict()
    for i in range(len(dataAP)):
        APPlotsArray[i],=APSubplots[i].plot(time,dataAP[i],'b-',label=f"DP{str(i)}")
    return APPlotsArray
def setDPPlots(dataDP=[],DPSubplots=[]):
    global time
    DPPlotsArray = dict()
    for i in range(len(dataDP)):
        DPPlotsArray[i],=DPSubplots[i].plot(time,dataDP[i],'b-',label=f"AP{str(i)}")
    return DPPlotsArray

def updateData(self):
    global time
    global dataDP
    global dataAP
    global DPSubplot
    global APSubplot
    global device
    global DPArray
    global APArray
    global DPPlotsArray
    global APPlotsArray
    global dataAPArray
    global dataDPArray
    DPPlotsDictArray = dict()
    APPlotsDictArray = dict()
    convertedAPArray=[]
    convertedDPArray=[]
    ret = device.read(0x81, 23,520)
    receiveData(ret)
    convertedAPArray=(i *0.000806 for i in APData)
    convertedDPArray=(i *3.3 for i in DPData)
    # # #appending the data into an array

    for i, x in enumerate(convertedAPArray, 0):
        dataAPArray[i].append(x)

    for i, x in enumerate(convertedDPArray, 0):
        dataDPArray[i].append(x)

    if len(time)==0:
        time = append(time,timeDiff*0.016384)
    else :
        time = append(time, time[-1]+timeDiff * 0.016384)
    # #set data
    # for i in range(TotalNumofDP):
    #     DPSubplot[DPArray[i]]=plt.set_data(time,dataDP)
    #for i in range(TotalNumofAP):
    # APPlotsDictArray[0]= APSubplot[0].plot(time,dataAP,label=APArray[0])

    #
    if time[-1] >= xmax-10.00:
        for i in range(TotalNumofDP):
            DPSubplot[i].axes.set_xlim(time[-1] - xmax + 1.0, time[-1] + 1.0)
        for i in range(TotalNumofAP):
            APSubplot[i].axes.set_xlim(time[-1] - xmax + 1.0, time[-1] + 1.0)
    return DPSubplot,APSubplot


def main():
    global TotalNumofDP
    global TotalNumofAP
    global DPSubplot
    global APSubplot
    global device
    global DPArray
    global APArray
    global DPPlotsArray
    global APPlotsArray
    global dataAP
    print("Welcome to XXX\n")
    device =findUSBNConfig()
    NumofDP=keyInDP()
    TotalNumofDP = len(NumofDP)

    NumofAP=keyInAP()
    TotalNumofAP = len(NumofAP)

    # take value configured and plot graph
    # Sent for figure
    font = {'size': 9}
    matplotlib.rc('font', **font)

    # Setup figure and subplots
    f0 = plt.figure(figsize=(15, 15))  # )

    # f0 = figure(num = 0, figsize = (12, 8))#, dpi = 100)
    f0.suptitle("Logic Analyzer", fontsize=12)

    # plot subplot
    odd = 1
    even = 2
    for i, num in enumerate(NumofDP, 0):
        # append the str DP and the number
        DPArray.append(f"DP{str(num)}")
        DPPlotsArray.append(f"pAP{str(num)}")
        if odd == 1:
            DPSubplot[i] = plt.subplot(TotalNumofDP, 2, odd)
        else:
            DPSubplot[i] = plt.subplot(TotalNumofDP, 2, odd, sharex=DPSubplot[0])
            plt.setp(DPSubplot[i-1].get_xticklabels(), visible=False)
        DPSubplot[i].set_ylim(0, 5)
        DPSubplot[i].set_xlim(0, 10)
        DPSubplot[i].set_ylabel(DPArray[i], rotation=0)
        odd += 2

    for i, num in enumerate(NumofAP, 0):
        # append the str AP and the number
        APArray.append(f"AP{str(num)}")
        APPlotsArray.append(f"pAP{str(num)}")
        if even == 2:
            APSubplot[i] = plt.subplot(TotalNumofAP, 2, even)
        else:
            APSubplot[i] = plt.subplot(TotalNumofAP, 2, even, sharex=APSubplot[0])
            plt.setp(APSubplot[i-1].get_xticklabels(), visible=False)
        APSubplot[i].set_ylim(0, 5)
        APSubplot[i].set_xlim(0, 10)
        APSubplot[i].set_ylabel(APArray[i], rotation=0)
        even += 2
    APPlotsArray=setAPPlots(dataAP, APSubplot)
    DPPlotsArray=setDPPlots(dataDP, DPSubplot)
    # set to full screen
    manager = plt.get_current_fig_manager()
    manager.window.state('zoomed')
    plt.subplots_adjust(hspace=0)


    # send out configuration
    DPCompressedPort = PortCompressFunc(DIGITAL, NumofDP)
    APCompressedPort = PortCompressFunc(ANALOG, NumofAP)
    configuration = bytes([STATE_CONFIG, 4, getUpperByte(DPCompressedPort), getLowerByte(DPCompressedPort), getUpperByte(APCompressedPort),
                           getLowerByte(APCompressedPort)])

    device.write(1, configuration, 200)


    simulation = animation.FuncAnimation(f0, updateData, blit=False, frames=None, interval=1, repeat=False)
    plt.show()


if __name__=="__main__":
    main()