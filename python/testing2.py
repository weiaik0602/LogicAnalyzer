from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation
import numpy as np
from matplotlib import gridspec

import usb.core
import usb.util
import usb.backend.libusb0 as libusb0

#define USB backend
from ctypes import*
backend = usb.backend.libusb0.get_backend(find_library=lambda x: "C:\\WINDOWS\\system32\\libusb-1.0.dll")

#find device(STM32 CDC device)	idVendor=0x0483, idProduct=0x5740
# device=usb.core.find(idVendor=0x0483, idProduct=0x5740,backend=backend)
# if device is None:
#     raise ValueError('No device found.')
# else:
#     print("Device is found")
#     device.set_configuration()


# Sent for figure
font = {'size': 9}
matplotlib.rc('font', **font)

# Setup figure and subplots
f0 = figure(num = 0, figsize = (12, 8))#, dpi = 100)
f0.suptitle("Logic Analyzer", fontsize=12)

dp00 = subplot2grid((2, 2), (0, 0))
dp01 = subplot2grid((2, 2), (1, 0))

ap00 = subplot2grid((2, 2), (0, 1))
ap01 = subplot2grid((2, 2), (1, 1))

#tight_layout()

# Set titles of subplots
dp00.set_title('Voltage vs Time')
dp01.set_title('Voltage vs Time')
ap00.set_title('Voltage vs Time')
ap01.set_title('Voltage vs Time')


# set y-limits
dp00.set_ylim(0,5)
ap00.set_ylim(0,5)
dp01.set_ylim(0,5)
ap01.set_ylim(0,5)

# sex x-limits
dp00.set_xlim(0,10.0)
ap00.set_xlim(0,10.0)
dp01.set_xlim(0,10.0)
ap01.set_xlim(0,10.0)



# Turn on grids
dp00.grid(True)
ap00.grid(True)
dp01.grid(True)
ap01.grid(True)


# set label names
dp00.set_xlabel("Time")
dp00.set_ylabel("Voltage")
ap00.set_xlabel("Time")
ap00.set_ylabel("Voltage")
dp01.set_xlabel("Time")
dp01.set_ylabel("Voltage")
ap01.set_xlabel("Time")
ap01.set_ylabel("Voltage")

# Data Placeholders
dataDP00=zeros(0)
dataAP00=zeros(0)
dataDP01=zeros(0)
dataAP01=zeros(0)
t=zeros(0)

# set plots
pDP00, = dp00.plot(t,dataDP00,'b-', label="DP0")
pAP00, = ap00.plot(t,dataAP00,'g-', label="AP0")
pDP01, = dp01.plot(t,dataDP01,'b-', label="DP1")
pAP01, = ap01.plot(t,dataAP01,'g-', label="AP1")

# set lagends
dp00.legend([pDP00], [pDP00.get_label()])
ap00.legend([pAP00], [pAP00.get_label()])
dp01.legend([pDP01], [pDP01.get_label()])
ap01.legend([pAP01], [pAP01.get_label()])

# Data Update
xmin = 0.0
xmax = 10.0
x = 0.0


def updateData(self):
    global x
    global dataDP00
    global dataAP00
    global dataDP01
    global dataAP01
    global t


    # msg = 'test'
    # device.write(1, msg, 100)
    # ret = device.read(0x81, 23, 550)
    # time = ((ret[0] << 8) | ret[1])
    # if ret[2]==1:
    #     dAP00 = (ret[3] << 8) | ret[4]
    #     dAP01 = (ret[5] << 8) | ret[6]
    #     # dDP00 = dataDP00[-1]
    #     # dDP01 = dataDP01[-1]
    # dDP00 = ret[3]
    # dDP01 = ret[3]
    #
    # dAP00 = dAP00 * 0.000806
    # dAP01 = dAP01 * 0.000806
    #
    # dDP00=dDP00*3.3
    # dDP01 = dDP01 * 3.3



    dataDP00 = append(dataDP00, 0)
    dataDP01 = append(dataDP01, 1)
    dataAP00 = append(dataAP00, 0)
    dataAP01 = append(dataAP01, 1)

    #rtime=time/2
    #rtime=x     #fake the time as the interrupt time is not working
    t=append(t,x)
    x+=0.5
    pDP00.set_data(t,dataDP00)
    pAP00.set_data(t,dataAP00)
    pDP01.set_data(t, dataDP01)
    pAP01.set_data(t, dataAP01)


    if t[-1] >= xmax-10.00:
        pDP00.axes.set_xlim(t[-1] - xmax + 1.0, t[-1] + 1.0)
        pAP00.axes.set_xlim(t[-1] - xmax + 1.0, t[-1] + 1.0)
        pDP01.axes.set_xlim(t[-1] - xmax + 1.0, t[-1] + 1.0)
        pAP01.axes.set_xlim(t[-1] - xmax + 1.0, t[-1] + 1.0)

    return pDP00,pAP00,pDP01,pAP01


fig = plt.figure()
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])
# interval: draw new frame every 'interval' ms
# frames: number of frames to draw
simulation = animation.FuncAnimation(f0, updateData, blit=False, frames=None, interval=1, repeat=False)


plt.show()
