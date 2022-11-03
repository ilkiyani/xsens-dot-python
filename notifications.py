'''
This class allows a Python script to listen for data from an Xsens DOT.

You can attach this "delegate" to an Xsens DOT with `Peripheral.setDelegate()`.
NOTE: We give the Delegate class the address so it can print which device
      the data came from.
For example:
    my_periph = Peripheral("ab:cd:ef:12:34:56")
    delegate = XsensNotificationDelegate(my_periph.addr)
    my_periph.setDelegate(
'''

from bluepy import btle
import numpy as np
import sys
import getopt

import time
from random import random as rand

from pylsl import StreamInfo, StreamOutlet, local_clock
class XsensNotificationDelegate(btle.DefaultDelegate):
    def __init__(self, bluetooth_device_address):
        btle.DefaultDelegate.__init__(self)
        self.bluetooth_device_address = bluetooth_device_address
        print("XsensNotificationDelegate has been initialized")

    # Do something when sensor data is received. In this case, print it out.
    def handleNotification(self, cHandle, data):
        data_segments = np.dtype([('timestamp', np.uint32), ('quat_w', np.float32), ('quat_x', np.float32),
                       ('quat_y', np.float32), ('quat_z', np.float32)])
        human_readable_data = np.frombuffer(data, dtype=data_segments)
        formatted_data = str([x for x in human_readable_data.tolist()[0]][:-1])[1:-1]
        formatted_data = self.bluetooth_device_address + ", " + formatted_data
        print(formatted_data)
        srate = 60
        name = 'Dot'
        type = 'XSENS'
        n_channels = 1
    # first create a new stream info (here we set the name to BioSemi,
    # the content-type to EEG, 8 channels, 100 Hz, and float-valued data) The
    # last value would be the serial number of the device or some other more or
    # less locally unique identifier for the stream as far as available (you
    # could also omit it but interrupted connections wouldn't auto-recover)
        info = StreamInfo(name, type, n_channels, srate, 'float32', 'myuid34234')

    # next make an outlet
        outlet = StreamOutlet(info)

        print("now sending data...")
        start_time = local_clock()
        sent_samples = 0
        while True:
                elapsed_time = local_clock() - start_time
                required_samples = int(srate * elapsed_time) - sent_samples
                for sample_ix in range(required_samples):
            # make a new random n_channels sample; this is converted into a
            # pylsl.vectorf (the data type that is expected by push_sample)
                        mysample = formatted_data
            # now send it
                        outlet.push_sample(mysample)
                sent_samples += required_samples
        # now send it and wait for a bit before trying again.
                time.sleep(0.01)
