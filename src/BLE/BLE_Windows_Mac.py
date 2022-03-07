# https://bleak.readthedocs.io/en/latest/
# Installation: "pip install bleak"
from src.bluetoothDecoder import BluetoothDecoder
import asyncio
from bleak import BleakScanner, BleakClient
from bleak.exc import BleakError
from sys import platform

ble_obj = BluetoothDecoder()
devicesList = []
if platform != "Darwin":
    address = "00:A0:50:BA:C5:81"
else:
    address = "804f806f-a7e0-408c-83ca-4a2cfe1d5d51"
UUID = "804f806f-a7e0-408c-83ca-4a2cfe1d5d51"
#UUID = "00001801-0000-1000-8000-00805f9b34fb"
#UUID = "00001800-0000-1000-8000-00805f9b34fb
#UUID = "00002a24-0000-1000-8000-00805f9b34fb"

async def scanForDevices() -> None:
    devices = await BleakScanner.discover()
    i=0
    for d in devices:
        print(i, ": ", d)
        i=i+1
        devicesList.append(d)

async def getModel(addr: str) -> None:
    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")
        model_number = await client.read_gatt_char(UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

async def connectAndReadServices(ble_address: str) -> None:
    device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)
    if not device:
        raise BleakError(f"A device with address {ble_address} could not be found.")
    async with BleakClient(device) as client:
        print(f"Connected: {client.is_connected}")
        services = await client.get_services()
        print("Services:")
        for service in services:
            print(service)

async def connectAndReadCharacteristics(ble_address: str) -> None:
    async with BleakClient(ble_address) as client:
        print(f"Connected: {client.is_connected}")
        for service in client.services:
            print(f"[Service] {service}")
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = bytes(await client.read_gatt_char(char.uuid))
                        print(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}")

                    except Exception as e:
                        print(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {e}")

                else:
                    value = None
                    print(f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}")

async def connectAndGetData(addr, char_uuid):
    async with BleakClient(addr) as client:
        print(f"Connected: {client.is_connected}")

        await client.start_notify(char_uuid, notification_handler)
        await asyncio.sleep(50.0)
        await client.stop_notify(char_uuid)

def notification_handler(sender, data):
    """Notification handler which prints the data received."""
    print("{0}: {1}".format(sender, bytes(data)))

    #byteorder=sys.byteorder
    print(bin(int.from_bytes(data, byteorder="big")).strip('0b'))

    f = open("logFile.txt", 'a')
    f.write(str(bytes(data)))
    f.write("\n")
    f.close()

    ble_obj.addNextByte(bytes(data))

def getDeviceAddress():
    asyncio.run(scanForDevices())
    choice = 'r'
    while choice == 'r':
        print(devicesList)
        choice = input("Enter desired device: ")
    if platform == "Darwin":
        return devicesList[int(choice)].metadata["uuids"]
    return devicesList[int(choice)].address

if __name__ == "__main__":
#    address = getDeviceAddress()
    print("Address: ", address)
    print("UUID: ", UUID)
    #asyncio.run(getModel(address))
    #asyncio.run(connectAndReadServices(address))
    #asyncio.run(connectAndReadCharacteristics(address))
    asyncio.run(connectAndGetData(address,UUID))
    for i in range(10):
        print(ble_obj.getNextPoint())
        # SW2 = mode change
        # Light -> Volt -> Amm -> Ohm -> Temp