import asyncio
from bleak import BleakScanner, BleakClient
from bleak.exc import BleakError

devicesList = []
address = ""
UUID = "00002a24-0000-1000-8000-00805f9b34fb"

async def scanForDevices() -> None:
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)
        devicesList.append(d)

async def getModel(addr: str) -> None:
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

async def connectAndReadServices(ble_address: str) -> None:
    device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)
    if not device:
        raise BleakError(f"A device with address {ble_address} could not be found.")
    async with BleakClient(device) as client:
        svcs = await client.get_services()
        print("Services:")
        for service in svcs:
            print(service)

if __name__ == "__main__":
    asyncio.run(scanForDevices())
    choice = input("Enter desired device: ")
    address = devicesList[int(choice)].address
    #UUID = devicesList[int(choice)].metadata["uuids"][0]
    print(address)
    print(UUID)
    asyncio.run(getModel(address))
    asyncio.run(connectAndReadServices(address))