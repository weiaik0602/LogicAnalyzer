import usb.core

print(usb.core.show_devices())
device=usb.core.find(backend = None, custom_match = None    \
                     ,bcdUSB=0x0110,bDeviceClass=0xFF,bDeviceSubClass=0x00  \
                     ,bDeviceProtocol=0x00,bMaxPacketSize0=0x08,idVendor=0x1A86    \
                     ,idProduct=0x7523,bcdDevice=0x0254,iManufacturer=0x00,iProduct=0x02    \
                     ,iSerialNumber=0x00,bNumConfigurations=0x01,bNumInterfaces=0x01)

if device is None:
    print('Not found')
else:
    print('Found')
    print(device)

dev=usb.core.find(idVendor=0x0483, idProduct=0x5740)
if dev is None:
    print('Not found')
else:
    print('Found')
    print(dev)

   # device.set_configuration()
