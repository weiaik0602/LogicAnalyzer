import

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
value = [0x80,0x28,0xD8,0xFA]
x=breakTimeData(value)


# def breakDataForAP(value=[]):
#     global APData=[]
#     dataCounter=breakTimeData(value)


