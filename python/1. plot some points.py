
import sys
import time
import numpy as np
from IPython import get_ipython
ipy = get_ipython()
if ipy is not None:
    ipy.run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
dev = usb.core.find(idVendor=0x046D, idProduct=0xC07E)

units=input("pls input ur unit C: ")
units=units.upper()
if not(units=='C'):
    print("invalid unit --> "+ units)
    print("prog is now exiting")
    sys.exit()

print("enter ur temp, key in non-num if ur done")
#store the time and temp by creating an empty array
stime=np.array([])
stemp=np.array([])


while True:
    #ask for new temp
    temp=input("Input temp is "+units+" : ")
    #validate the input if it is a num?
    try:
        temp=float(temp)
        print("value stored!!!")
    #if not come out from the loop
    except:
        print("all temp taken, ploting graph")
        break
    
    newTime= time.clock()

    #store the values
    stime=np.append(stime,newTime)
    stemp=np.append(stemp,temp)
    
plt.plot(stime,stemp,'ro')
plt.xlabel("Time(sec)")
plt.ylabel("Temp(C)")
plt.show()

print("Max temp : "+str(np.max(stemp)))
print("Min temp : "+str(np.min(stemp)))
print("Mean temp : "+str(np.mean(stemp)))


      
