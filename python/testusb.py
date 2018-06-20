import usb.core
import usb.util

def main():
    device = usb.core.find(find_all=True, idVendor=0x1A86, idProduct=0x7523)
    #print(usb.core.show_devices())
    if device is None:
        print('Device not found')
    else:
        print('found')
    # use the first/default configuration
    device.set_configuration()
    print('a')
    # first endpoint
    endpoint = device[0][(0,0)][0]

    # read a data packet
    data = None
    collected=0
    attempts=50
    #stop_request=input("Press Enter to stop it")
    longdata="abc;efg;egw;sdg"
    shortdata=longdata.split(';')
    s1=shortdata[0]
    s2=shortdata[1]
    print(s1)
    print(s2)
    while collected<50:
        try:
            data = device.read(endpoint.bEndpointAddress,
                               endpoint.wMaxPacketSize)
            print(data)
            collected+=1

        except usb.core.USBError as e:
            data = None
            if e.args == ('Operation timed out',):

                continue

if __name__ == '__main__':
  main()