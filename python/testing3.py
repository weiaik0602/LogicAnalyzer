import usb.core
import usb.util

def main():
    device=usb.core.find(idVendor=0x0483, idProduct=0x5740)


    if device is None:
        print('Not found')
    else:
        print('Found')
        #print(device)
        device.set_configuration()
    #     endpoint = device[0][(0, 0)][0]
    # collected = 0
    # attempts = 50
    # while collected<attempts:
    #     try:
    #         data = device.read(endpoint.bEndpointAddress,
    #                            endpoint.wMaxPacketSize)
    #         print(data)
    #         collected+=1
    #
    #     except usb.core.USBError as e:
    #         data1 = device.read(endpoint.bEndpointAddress,
    #                            endpoint.wMaxPacketSize)
    #         data1 = None
    #         collected += 1
    #         print(data1)
    #         if e.args == ('Operation timed out',):
    #
    #             continue

if __name__ == '__main__':
  main()