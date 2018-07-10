# Uncomment the next two lines if you want to save the animation
#import matplotlib
#matplotlib.use("Agg")

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
    #device set config
    device.set_configuration()


# Sent for figure
font = {'size'   : 9}
matplotlib.rc('font', **font)

# Setup figure and subplots
f0 = figure(num = 0, figsize = (12, 8))#, dpi = 100)
f0.suptitle("Oscillation decay", fontsize=12)
ax01 = subplot2grid((2, 2), (0, 0))
ax02 = subplot2grid((2, 2), (0, 1))
ax03 = subplot2grid((2, 2), (1, 0), colspan=2, rowspan=1)
ax04 = ax03.twinx()
#tight_layout()

# Set titles of subplots
ax01.set_title('Position vs Time')
ax02.set_title('Velocity vs Time')
ax03.set_title('Position and Velocity vs Time')

# set y-limits
ax01.set_ylim(0,2)
ax02.set_ylim(-6,6)
ax03.set_ylim(-0,5)
ax04.set_ylim(-10,10)

# sex x-limits
ax01.set_xlim(0,5.0)
ax02.set_xlim(0,5.0)
ax03.set_xlim(0,5.0)
ax04.set_xlim(0,5.0)

# Turn on grids
ax01.grid(True)
ax02.grid(True)
ax03.grid(True)

# set label names
ax01.set_xlabel("x")
ax01.set_ylabel("py")
ax02.set_xlabel("t")
ax02.set_ylabel("vy")
ax03.set_xlabel("t")
ax03.set_ylabel("py")
ax04.set_ylabel("vy")

# Data Placeholders
yp1=zeros(0)
yv1=zeros(0)
yp2=zeros(0)
yv2=zeros(0)
t=zeros(0)

# set plots
p011, = ax01.plot(t,yp1,'b-', label="yp1")
p012, = ax01.plot(t,yp2,'g-', label="yp2")

p021, = ax02.plot(t,yv1,'b-', label="yv1")
p022, = ax02.plot(t,yv2,'g-', label="yv2")

p031, = ax03.plot(t,yp1,'b-', label="yp1")
p032, = ax04.plot(t,yv1,'g-', label="yv1")
print(type(p011))
# set lagends
ax01.legend([p011,p012], [p011.get_label(),p012.get_label()])
ax02.legend([p021,p022], [p021.get_label(),p022.get_label()])
ax03.legend([p031,p032], [p031.get_label(),p032.get_label()])

# Data Update
xmin = 0.0
xmax = 5.0
x = 0.0

def updateData(self):
    global x
    global yp1
    global yv1
    global yp2
    global yv2
    global t

    ret = device.read(0x81, 1, 100)
    sret = ''.join([chr(x) for x in ret])
    sret = bytes(sret, 'utf-8')
    sret=ord(sret)
    tmpp1 = 1 + exp(-x) *sin(2 * pi * x)
    tmpv1 = - exp(-x) * sin(2 * pi * x) + exp(-x) * cos(2 * pi * x) * 2 * pi
    yp1=append(yp1,sret)
    yv1=append(yv1,sret)
    yp2=append(yp2,0.5*tmpp1)
    yv2=append(yv2,0.5*tmpp1)
    t=append(t,x)

    x += 0.05

    p011.set_data(t,yp1)
    p012.set_data(t,yp2)

    p021.set_data(t,yv1)
    p022.set_data(t,yv2)

    p031.set_data(t,yp1)
    p032.set_data(t,yv1)

    if x >= xmax-1.00:
        p011.axes.set_xlim(x-xmax+1.0,x+1.0)
        p021.axes.set_xlim(x-xmax+1.0,x+1.0)
        p031.axes.set_xlim(x-xmax+1.0,x+1.0)
        p032.axes.set_xlim(x-xmax+1.0,x+1.0)

    return p011, p012, p021, p022, p031, p032

# interval: draw new frame every 'interval' ms
# frames: number of frames to draw
simulation = animation.FuncAnimation(f0, updateData, blit=False, frames=200, interval=20, repeat=False)

# Uncomment the next line if you want to save the animation
#simulation.save(filename='sim.mp4',fps=30,dpi=300)

plt.show()
