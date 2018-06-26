# Uncomment the next two lines if you want to save the animation
#import matplotlib
#matplotlib.use("Agg")

import numpy
from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation



# Sent for figure
font = {'size'   : 9}
matplotlib.rc('font', **font)

# Setup figure and subplots
f0 = figure(num = 0, figsize = (12, 8))#, dpi = 100)
f0.suptitle("Logic Analyzer", fontsize=12)
ax01 = subplot2grid((2, 2), (0, 0))

# Set titles of subplots
ax01.set_title('Voltage vs Time')

# set y-limits
ax01.set_ylim(0,3.3)

# sex x-limits
ax01.set_xlim(0,5.0)

# Turn on grids
ax01.grid(True)

# set label names
ax01.set_xlabel("Time")
ax01.set_ylabel("Voltage")

# Data Placeholders
yp1=zeros(0)
# yv1=zeros(0)
yp2=zeros(0)
# yv2=zeros(0)
t=zeros(0)

# set plots
p011, = ax01.plot(t,yp1,'b-', label="port1")
p012, = ax01.plot(t,yp2,'g-', label="line2")

# set lagends
ax01.legend([p011], [p011.get_label()])

# Data Update
xmin = 0.0
xmax = 5.0
x = 0.00

def updateData(self):
	global x
	global yp1
	global yp2
	global t

	tmpp1 = 1 + 1
	yp1=append(yp1,tmpp1)
	yp2=append(yp2,0.5*tmpp1)
	t=append(t,x)

	x += 0.05

	p011.set_data(t,yp1)
	p012.set_data(t,yp2)



	if x >= xmax-1.00:
		p011.axes.set_xlim(x-xmax+1.0,x+1.0)


	return p011, p012,# p021, p022, p031, p032

# interval: draw new frame every 'interval' ms
# frames: number of frames to draw
simulation = animation.FuncAnimation(f0, updateData, blit=False, frames=200, interval=20, repeat=False)

# Uncomment the next line if you want to save the animation
#simulation.save(filename='sim.mp4',fps=30,dpi=300)

plt.show()
