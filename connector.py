# scanner.py
from bleak import BleakScanner

async def scan_for_devices():
    devices = await BleakScanner.discover()
    return devices
