# i am in scanner.py
from bleak import BleakScanner

# function to scan for devices (bletooth)
async def scan_for_devices():
    devices = await BleakScanner.discover()
    return devices
