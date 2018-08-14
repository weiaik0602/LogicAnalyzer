from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import usb.core
import usb.util
import usb.backend.libusb0 as libusb0

#define USB backend
from ctypes import*
backend = usb.backend.libusb0.get_backend(find_library=lambda x: "C:\\WINDOWS\\system32\\libusb-1.0.dll")

#find device(STM32 CDC device)	idVendor=0x0483, idProduct=0x5740
device=usb.core.find(idVendor=0x0483, idProduct=0x5740,backend=backend)
# if device is None:
#     raise ValueError('No device found.')
# else:
#     print("Device is found")
#     device.set_configuration()


# Sent for figure
font = {'size': 9}
matplotlib.rc('font', **font)

# Setup figure and subplots
f0=plt.figure(figsize = (15, 15))#)

#f0 = figure(num = 0, figsize = (12, 8))#, dpi = 100)
f0.suptitle("Logic Analyzer", fontsize=12)

dp00 = plt.subplot(10, 2, 1)
dp01 = plt.subplot(10, 2, 3,sharex=dp00)
plt.setp(dp00.get_xticklabels(), visible=False)

ap00 = plt.subplot(5, 2, 2)
ap01 = plt.subplot(5, 2, 4,sharex=ap00)

#set to full screen
manager = plt.get_current_fig_manager()
manager.window.state('zoomed')


# Set titles of subplots
# dp00.set_title('Voltage vs Time')
# dp01.set_title('Voltage vs Time')
# ap00.set_title('Voltage vs Time')
# ap01.set_title('Voltage vs Time')


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
# dp00.grid(True)
# ap00.grid(True)
# dp01.grid(True)
# ap01.grid(True)


# set label names
# dp00.set_xlabel("Time")
dp00.set_ylabel("DP0",rotation=0)
# ap00.set_xlabel("Time")
ap00.set_ylabel("AP0",rotation=0)
# dp01.set_xlabel("Time")
dp01.set_ylabel("DP1",rotation=0)
# ap01.set_xlabel("Time")
ap01.set_ylabel("AP0",rotation=0)

# Data Placeholders
dataDP00=zeros(0)
dataAP00=zeros(0)
dataDP01=zeros(0)
dataAP01=zeros(0)
t=zeros(0)

# set plots
print(type(dp00))
print(dp00)
pDP00,  = dp00.plot(t,dataDP00,'b-', label="DP0")
pAP00,  = ap00.plot(t,dataAP00,'g-', label="AP0")
pDP01, = dp01.plot(t,dataDP01,'b-', label="DP1")
pAP01, = ap01.plot(t,dataAP01,'g-', label="AP1")
print(type(pDP00))
# set lagends
# dp00.legend([pDP00], [pDP00.get_label()])
# ap00.legend([pAP00], [pAP00.get_label()])
# dp01.legend([pDP01], [pDP01.get_label()])
# ap01.legend([pAP01], [pAP01.get_label()])

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
    #
    #
    # dDP00 = ret[3]
    # dDP01 = ret[3]
    #
    # dAP00 = dAP00 * 0.000806
    # dAP01 = dAP01 * 0.000806
    #
    # dDP00=dDP00*3.3
    # dDP01 = dDP01 * 3.3



    dataDP00 = append(dataDP00, 1)
    dataDP01 = append(dataDP01, 1)
    dataAP00 = append(dataAP00, 1)
    dataAP01 = append(dataAP01, 1)

    # rtime=time/2
    #rtime=x     #fake the time as the interrupt time is not working
    t=append(t,x)
    x+=0.5
    print(type(pDP00))
    pDP00.set_data(t,dataDP00)
    pAP00.set_data(t,dataAP00)
    pDP01.set_data(t, dataDP01)
    pAP01.set_data(t, dataAP01)
    print(type(t))
    print(type(dataAP01))


    if t[-1] >= xmax:
        pDP00.axes.set_xlim(t[-1] - xmax + (xmax/10), t[-1] +  (xmax/10))
        pAP00.axes.set_xlim(t[-1] - xmax + (xmax/10), t[-1] +  (xmax/10))
        pDP01.axes.set_xlim(t[-1] - xmax +  (xmax/10), t[-1] +  (xmax/10))
        pAP01.axes.set_xlim(t[-1] - xmax +  (xmax/10), t[-1] +  (xmax/10))

    return pDP00,pAP00,pDP01,pAP01

# fig=plt.figure()
# interval: draw new frame every 'interval' ms
# frames: number of frames to draw
simulation = animation.FuncAnimation(f0, updateData, blit=False, frames=None, interval=1, repeat=False)

plt.show()
