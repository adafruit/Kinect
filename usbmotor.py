import usb.core
import usb.util
import sys
import time

# find our device
dev = usb.core.find(idVendor=0x045e, idProduct=0x02B0)

# was it found?
if dev is None:
    raise ValueError('Device not found')

for cfg in dev:
    sys.stdout.write("Configuration #"+str(cfg.bConfigurationValue) + '\n')
    for intf in cfg:
        sys.stdout.write('\tInterface #' + \
                         str(intf.bInterfaceNumber) + \
                         '\t, Alternate setting ' + \
                         str(intf.bAlternateSetting) + \
                         '\n')
        sys.stdout.write("\tEndpoints:\n")
        for ep in intf:
            sys.stdout.write('\t\t' + \
                             str(ep.bEndpointAddress) + \
                             '\n')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()


# test of reading data from different request #
#bRequest = 8         # or 8 or 9
#for i in range(255):
#    try:
#        ret = dev.ctrl_transfer(0x80, bRequest, i, 0, 4)
#        print i,
#        print ret
#    except:
#        # failed to get data for this request
#        pass



# (bmRequestType, bmRequestType, bmRequest, wValue, wIndex, nBytes)
ret = dev.ctrl_transfer(0xC0, 0x10, 0x0, 0x0, 1)
print hex(ret[0])   # should return 0x22 but dont know why ?

while True:
    # Get accel data
    ret = dev.ctrl_transfer(0xC0, 0x32, 0x0, 0x0, 10)
    #print map(hex, ret)

    # bytes 0 & 1 are always zero
    
    x = (ret[2] << 8) | ret[3]
    x = (x + 2**15) % 2**16 - 2**15     # convert to signed 16b
    y = (ret[4] << 8) | ret[5]
    y = (y + 2**15) % 2**16 - 2**15     # convert to signed 16b
    z = (ret[6] << 8) | ret[7]
    z = (z + 2**15) % 2**16 - 2**15     # convert to signed 16b
    
    print x, "\t", y, "\t", z

