# https://bleak.readthedocs.io/en/latest/
# Installation: "pip install bleak"
import asyncio
from email.utils import getaddresses
from typing import List
from bleak import BleakScanner, BleakClient
from bleak.exc import BleakError
from sys import platform

class BLE():

    ble_obj = None
    address = None
    UUID = None
    client = None
    continueBleData = False
    devicesList = []
    choice = None

    async def scanForDevices(self) -> List:
        """ Scan and get a list of nearby ble connections
            Args: 
                None
            Return: 
                List
        """
        devices = await BleakScanner.discover()
        return devices

    async def connectAndGetData(self) -> None:
        """ Connect to desired device and read data from it continuously
            Args: 
                addr (str): Address of ble device to connect to
                char_uuid (str): Designated UUID of device's data service
            Return: 
                None
        """
        async with BleakClient(self.address) as self.client:
            print(f"Connected: {self.client.is_connected}")
            # Get UUID for notify service
            for service in self.client.services:
                for char in service.characteristics:
                    if "notify" in char.properties:                
                        self.UUID = char.uuid
                            
            print("Address: ", self.address)
            print("UUID: ", self.UUID)
            self.continueBleData = True
            
            # Get data until disconnect signal given
            while self.continueBleData:
                await self.client.start_notify(self.UUID, self.notification_handler)
                #await asyncio.sleep(1.0)
                await self.client.stop_notify(self.UUID)
            
            # Disconnect from device
            await self.client.disconnect()
            print(f"Connected: {self.client.is_connected}")

    def notification_handler(self, sender, data) -> None:
        """ Notification handler which prints the data received.
            Args: 
                sender (str): [Unused] Representation of which device sent data
                data (str): Data received over bluetooth
            Return:
                None
        """
        print("{0}: {1}".format(sender, bytes(data)))
        self.ble_obj.addNextByte(bytes(data))

    def printDeviceList(self) -> None:
        """ Print a list of ble devices
            Args: 
                devices (List): List of all available ble devices 
            Return:
                None
        """
        i=0
        for d in self.devicesList:
            print(i, ": ", d)
            i=i+1

    def decodeAddressFromList(self) -> str:
        """ Return address of selected device, depending on OS
            Args: 
                choice (int): User selected device to connect to
                devices (List): List of all available ble devices 
            Return:
                address (str): Either string of address or UUID of device (Mac only)
        """
        if platform == "Darwin":
            return self.devicesList[int(self.choice)].metadata["uuids"]
        else:
            return self.devicesList[int(self.choice)].address

    def startBluetoothConnection(self, decoder) -> None:
        self.ble_obj = decoder
        self.devicesList = asyncio.run(self.scanForDevices())
        self.printDeviceList()
        self.choice = input("Enter desired device: ")
        self.address = self.decodeAddressFromList()
        if self.address != None:
            asyncio.run(self.connectAndGetData())
    
    def getConnectionStatus(self) -> bool: 
        return self.client.is_connected
    
    def disconnectFromDevice(self) -> None:
        self.continueBleData = False




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Unused functions that may be of use later
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
async def connectAndReadServices(ble_address: str) -> None:
    """ Connect to desired device to read and print out the services of the device
        Args: 
            ble_address (str): Address of ble device to connect to
        Return: 
            None
    """
    device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)
    if not device:
        raise BleakError(f"A device with address {ble_address} could not be found.")
    async with BleakClient(device) as client:
        print(f"Connected: {client.is_connected}")
        services = await client.get_services()
        print("Services:")
        for service in services:
            print(service)

async def connectAndReadCharacteristics(ble_address: str) -> str:
    """ Connect to desired device to read and print out the characteristics of the device. Return UUID for data
        Args: 
            ble_address (str): Address of ble device to connect to
        Return: 
            UUID (str): UUID of characteristic to use for reading data
    """
    async with BleakClient(ble_address) as client:
        print(f"Connected: {client.is_connected}")
        for service in client.services:
            print(f"[Service] {service}")
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = bytes(await client.read_gatt_char(char.uuid))
                        print(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}")
                        if 'notify' in char.properties:
                            print(char.properties)
                            print(char.uuid)
                            return char.uuid

                    except Exception as e:
                        print(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {e}")

                else:
                    value = None
                    print(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}")

async def getModel(addr: str) -> None:
    """ Connect to desired device to read and print out model number
        Args: 
            addr (str): Address of ble device to connect to
        Return: 
            None
    """
    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")
        model_number = await client.read_gatt_char(UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))