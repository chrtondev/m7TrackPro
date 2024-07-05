# i am in connector.py
from bleak import BleakClient
from datetime import datetime
from utils import clear_screen

HR_MEASUREMENT_UUID = "00002a37-0000-1000-8000-00805f9b34fb"

class HeartRateMonitor:
    def __init__(self):
        self.client = None
        self.data = []

    async def connect_to_device(self, device):
        self.client = BleakClient(device.address)
        await self.client.connect()
        await self.client.start_notify(HR_MEASUREMENT_UUID, self.notification_handler)
        clear_screen()
        print("Connected and receiving data...")

    def notification_handler(self, sender, data):
        heart_rate = self.decode_heart_rate(data)
        timestamp = datetime.now().strftime('%H:%M:%S.%f')
        timestamp = timestamp[:-3]  # Truncate microseconds to milliseconds
        self.data.append((timestamp, heart_rate))
        print(f"Received heart rate: {heart_rate} bpm at {timestamp}")

    def decode_heart_rate(self, data):
        flags = data[0]
        if flags & 0x01:
            heart_rate = int.from_bytes(data[1:3], byteorder='little')
        else:
            heart_rate = data[1]
        return heart_rate

    async def start_workout(self):
        self.data = []
        self.start_time = datetime.now()
        print("Workout started...")

    async def end_workout(self):
        end_time = datetime.now()
        duration = end_time - self.start_time
        print(f"Workout ended. Duration: {duration}")
        for timestamp, heart_rate in self.data:
            print(f"{timestamp}: {heart_rate} bpm")
        if self.client:
            await self.client.stop_notify(HR_MEASUREMENT_UUID)
            await self.client.disconnect()
            print("Disconnected from device.")
