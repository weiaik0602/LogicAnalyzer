import usb


device=usb.core.find(find_all=True)
print(usb.core.show_devices())
if device is None:
    print('Not found')
else:
    print('Found')
    print(list(device))