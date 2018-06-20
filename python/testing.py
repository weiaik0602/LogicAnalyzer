import usb.core
import usb.util

# find our device
dev = usb.core.find(find_all=True, idVendor=0x1A86, idProduct=0x7523)
usb.core.show_devices(find_all=True,idVendor=0x1A86, idProduct=0x7523)

# was it found?
if dev is None:
    print('Device not found')
else:
    print('found')
    for dev in dev:
        print("  idVendor: %d (0x%04x)" % (dev.idVendor, dev.idVendor))
        print("  idProduct: %d (0x%04x)" % (dev.idProduct, dev.idProduct))

# for bus in busses:
#   devices = bus.devices
#   for dev in devices:
#     print(repr(dev))
#     print("device:", dev.filename)
#     print ("  idvendor: %d (0x%04x)" % (dev.idvendor, dev.idvendor))
#     print ("  idproduct: %d (0x%04x)" % (dev.idproduct, dev.idproduct))
#     print ("manufacturer:", dev.imanufacturer)
#     print ("serial:", dev.iserialnumber)
#     print ("product:", dev.iproduct)
# print(usb.core.show_devices())