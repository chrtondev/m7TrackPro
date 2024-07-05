# i am in scanner.py
from bleak import BleakScanner

# function to scan for devices (bletooth)
async def scan_for_devices():
    devices = await BleakScanner.discover()
    return devices

# function used with the target device name inside of main.py
async def find_device_by_name(target_name):
    devices = await scan_for_devices()
    for device in devices:
        if device.name == target_name:
            return device
    return None
