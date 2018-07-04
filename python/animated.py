import numpy
from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation
import usb.core
import usb.util
import usb.backend.libusb0 as libusb0

#define USB backend
from ctypes import*
backend = usb.backend.libusb0.get_backend(find_library=lambda x: "C:\\WINDOWS\\system32\\libusb-1.0.dll")

#find device(STM32 CDC device)	idVendor=0x0483, idProduct=0x5740
device=usb.core.find(idVendor=0x0483, idProduct=0x5740,backend=backend)
if device is None:
    raise ValueError('No device found.')
else:
    print("Device is found")
    device.set_configuration()


# Sent for figure
font = {'size'   : 9}
matplotlib.rc('font', **font)

# Setup figure and subplots
f0 = figure(num = 0, figsize = (12, 8))#, dpi = 100)
f0.suptitle("Logic Analyzer", fontsize=12)
ax01 = subplot2grid((2, 2), (0, 0))
#tight_layout()

# Set titles of subplots
ax01.set_title('Voltage vs Time')


# set y-limits
ax01.set_ylim(0,5)


# sex x-limits
ax01.set_xlim(0,1000.0)


# Turn on grids
ax01.grid(True)


# set label names
ax01.set_xlabel("Time")
ax01.set_ylabel("Voltage")


# Data Placeholders
yp1=zeros(0)
t=zeros(0)

# set plots
p011, = ax01.plot(t,yp1,'b-', label="DP0")

# set lagends
ax01.legend([p011], [p011.get_label()])


# Data Update
xmin = 0.0
xmax = 1000.0
x = 0.0

def updateData(self):
    global x
    global yp1
    global t

    ret = device.read(0x81, 3, 100)
    time=(ret[2]<<8)|ret[1]
    data=ret[0]
    data=data*3.3
    yp1=append(yp1,data)
    stime=time/1000
    t=append(t,time)



    p011.set_data(t,yp1)




    if time >= xmax-100.00:
        p011.axes.set_xlim(time-xmax+100.0,time+100.0)

    return p011

# interval: draw new frame every 'interval' ms
# frames: number of frames to draw
simulation = animation.FuncAnimation(f0, updateData, blit=False, frames=None, interval=20, repeat=False)


plt.show()
