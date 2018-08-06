import usb.core
import usb.util
import usb.backend.libusb0 as libusb0

#define USB backend
from ctypes import*
backend = usb.backend.libusb0.get_backend(find_library=lambda x: "C:\\WINDOWS\\system32\\libusb-1.0.dll")

#find device(STM32 CDC device)	idVendor=0x0483, idProduct=0x5740
dev=usb.core.find(idVendor=0x0483, idProduct=0x5740,backend=backend)
if dev is None:
    raise ValueError('No device found.')
else:
    print("Device is found")
    dev.set_configuration()
cfg = dev.get_active_configuration()          # Get configuration descriptor
intf = cfg[(0,0)]                             # Get the 1st interface descriptor
ep = usb.util.find_descriptor(                # Get the 1st OUT endpoint descriptor
  intf,
  # match the first OUT endpoint
  custom_match = \
  lambda e: \
      usb.util.endpoint_direction(e.bEndpointAddress) == \
      usb.util.ENDPOINT_OUT)
print(ep)       # Print the OUT end-point
print(intf)                                  # Print the interface
print(cfg)                                   # Print the configuration

print(usb.core.util.get_string(dev, 1))             # Returns 'STMicroelectronics'
print(usb.core.util.get_string(dev, 2))             # Returns 'STM32 STLink'
print(usb.core.util.get_string(dev, 4))             # Returns 'ST Link'
