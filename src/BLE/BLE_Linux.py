# Pygattlib dependencies: https://github.com/oscaracena/pygattlib
from gattlib import DiscoveryService, GATTRequester, GATTResponse
import time
import sys

class Connect(object):
    def __init__(self, address):
        self.requester = GATTRequester(address, False)
        self.connect()

    def connect(self):
        print("Connecting...", end=' ')
        sys.stdout.flush()

        self.requester.connect(True)
        print("OK!")

class BluetoothConn():
    def __init__(self):
        self.service = DiscoveryService("hci0")
        self.devices = self.service.discover(2)

    def printListOfBleDevices(self):
        for address, name in self.devices.items():
            print("name: {}, address: {}".format(name, address))

 #   def getAddress(self):
 #       for address, name in self.devices.items():
 #           print("name: {}, address: {}".format(name, address))
 #       choice = input("Enter desired device number")
 #       self.addr = address[choice]
    
    def connectToDevice(self, addr):
        Connect(addr)
    
    def readDeviceDesc(self, addr):
        req = GATTRequester(addr)
        name = req.read_by_uuid("00002a00-0000-1000-8000-00805f9b34fb")[0]
        steps = req.read_by_handle(0x15)[0]

    def getData(self, addr):
        req = GATTRequester(addr)
        response = GATTResponse()

        while True:
            req.read_by_handle_async(0x15, response)
            # Wait for packets
            while not response.received():
                time.sleep(0.1)

            steps = response.received()[0]

ble = BluetoothConn()

# Prints list of nearby ble devices
ble.printListOfBleDevices()

# Get addr of device
#addr = ble.getAddr()
addr = "00:A0:50:BA:C5:81"

# Connect to device
ble.connectToDevice(addr)

# Read device description
ble.readDeviceDesc(addr)

# Get info over ble
ble.getData(addr)
