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
STATE_CHANGE_APP = 0x9
STATE_SEND_DP = 0xa
STATE_SEND_AP = 0xb
STATE_ASK_APP =0xe
DIGITAL = 0
ANALOG = 1
xmax = 5.0
#Global variable
timeDiff = 0
analogTick=0
APPeriod=0
APData = [0]
DPData = [0]
DPArray = list()
APArray = list()
DPPlotsArray = list()
APPlotsArray = list()
dataDP = dict()
dataAP = dict()
DPtime = zeros(0)
APtime = zeros(0)
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
        # if not come out from the loop
        except:
            print("all the port taken")
            break
        if DP<10:
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
        # if not come out from the loop
        except:
            print("all the port taken")
            break
        if AP<10:
            NumofAP.append(int(AP))
    return NumofAP
def keyInAPPeriod():
    print("Key in the AP period you wish to use")
    APPeriod=input()
    APPeriod = float(APPeriod)
    APPeriod = int(APPeriod)
    return APPeriod
def askDefaultAPPeriod():
    global device
    data = bytes([STATE_ASK_APP, 1,0])
    # print(list(configuration))
    device.write(1, data, 200)
    ret=device.read(0x81, 2,50)
    if ret[1]==STATE_ASK_APP:
        return ret[0]
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
def breakAPTimeData(value=[]):
    analogTick=value[-2]<<24|value[-3]<<16|value[-4]<<8|value[-5]<<0
    return analogTick
def breakDataForAP(USBData=[]):
    global APData
    global analogTick
    APData[:]=[]
    dataCounter=-5
    analogTick=breakAPTimeData(USBData)
    evencounter=0
    oddcounter=1
    counter=0
    max=len(USBData)+dataCounter
    while evencounter<(max):
        APData.insert(counter,USBData[oddcounter]<<8|USBData[evencounter])
        counter+=1
        evencounter += 2
        oddcounter += 2
def breakDataForDP(USBData=[]):
    global DPData
    global TotalNumofDP
    DPData[:]=[]
    DPtemp=0
    dataCounter = breakTimeData(USBData)
    counter = 0
    max = len(USBData) + dataCounter
    if USBData[dataCounter]==USBData[0]:
        DPtemp = USBData[0]
    else :
        DPtemp=USBData[dataCounter]<<8|USBData[0]
    for i in range (TotalNumofDP):
        DPData.insert(counter,DPtemp&0x01)
        counter+=1
        DPtemp>>=1
def receiveData(ret=[]):
    if ret[-1]==STATE_SEND_DP:
        breakDataForDP(ret)
    if ret[-1] == STATE_SEND_AP:
        breakDataForAP(ret)
    return ret[-1]
def setAPPlots(dataAP=[],APSubplots=[]):
    global APtime
    APPlotsArray = dict()
    for i in range(len(dataAP)):
        APPlotsArray[i],=APSubplots[i].plot(APtime,dataAP[i],'b-',label=f"AP{str(i)}")
    return APPlotsArray
def setDPPlots(dataDP=[],DPSubplots=[]):
    global DPtime
    DPPlotsArray = dict()
    for i in range(len(dataDP)):
        DPPlotsArray[i], = DPSubplots[i].plot(DPtime, dataDP[i], 'b-', label=f"DP{str(i)}")
    return DPPlotsArray

def updateData(self):
    global DPtime
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
    global TotalNumofDP
    global TotalNumofAP
    global APtime
    DPPlotsDictArray = dict()
    APPlotsDictArray = dict()
    convertedAPArray=[]
    convertedDPArray=[]
    ret = device.read(0x81, 23,520)
    state=receiveData(ret)
    convertedAPArray=(i *0.000806 for i in APData)
    convertedDPArray=(i *3.3 for i in DPData)
    # #appending the data into an array

    if len(APtime)==0:
        APtime = append(APtime,0)
    else :
        APtime = append(APtime, (analogTick*0.5))
        for i, x in enumerate(convertedAPArray, 0):
            dataAPArray[i].append(round(x,2))
    # print(list(dataAPArray[0]))

    if len(DPtime)==0:
        DPtime = append(DPtime,0)
    else :
        DPtime = append(DPtime, DPtime[-1]+round((timeDiff * 0.016384),2))
        for i, x in enumerate(convertedDPArray, 0):
            dataDPArray[i].append(x)
    # #set data
    for i in range(TotalNumofAP):
        APPlotsArray[i].set_data(APtime, dataAPArray[i])
    for i in range(TotalNumofDP):
        DPPlotsArray[i].set_data(DPtime, dataDPArray[i])

    if DPtime[-1] >= xmax:
        for i in range(TotalNumofDP):
            DPSubplot[i].axes.set_xlim(DPtime[-1] - xmax + (xmax/100), DPtime[-1] + (xmax/100))
    if APtime[-1] >= xmax:
        for i in range(TotalNumofAP):
            APPlotsArray[i].axes.set_xlim(APtime[-1] - xmax + (xmax/100), APtime[-1] +(xmax/100))
    return APPlotsArray,DPPlotsArray


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
    global APData
    global DPData
    global APPeriod
    print("Welcome to Logic Analyzer\n")
    device =findUSBNConfig()
    NumofDP=keyInDP()
    TotalNumofDP = len(NumofDP)

    NumofAP=keyInAP()
    TotalNumofAP = len(NumofAP)

    APPeriod=askDefaultAPPeriod()
    print("Currently the period for AP is ",APPeriod)
    APPeriod=keyInAPPeriod()

    APData = [0]*TotalNumofAP
    DPData = [0]*TotalNumofDP
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
        DPSubplot[i].set_xlim(0, xmax)
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
        APSubplot[i].set_xlim(0, xmax)
        APSubplot[i].set_ylabel(APArray[i], rotation=0)
        even += 2
    for i in range(TotalNumofDP) :
        dataDP[i]=zeros(0)
    for i in range(TotalNumofAP) :
        dataAP[i]=zeros(0)
    APPlotsArray=setAPPlots(dataAP, APSubplot)
    DPPlotsArray=setDPPlots(dataDP, DPSubplot)
    # set to full screen
    manager = plt.get_current_fig_manager()
    manager.window.state('zoomed')
    plt.subplots_adjust(hspace=0)


    # send out configuration
    DPCompressedPort = PortCompressFunc(DIGITAL, NumofDP)
    APCompressedPort = PortCompressFunc(ANALOG, NumofAP)
    configuration = bytes([STATE_CONFIG, 5, getUpperByte(DPCompressedPort), getLowerByte(DPCompressedPort),\
                           getUpperByte(APCompressedPort),getLowerByte(APCompressedPort),APPeriod])
    # print(list(configuration))
    device.write(1, configuration, 200)


    simulation = animation.FuncAnimation(f0, updateData, blit=False, frames=None, interval=1, repeat=False)
    plt.show()


if __name__=="__main__":
    main()