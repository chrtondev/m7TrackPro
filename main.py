# i am in main.py
import asyncio
from scanner import scan_for_devices
from connector import HeartRateMonitor

async def main():
    monitor = HeartRateMonitor()
    devices = await scan_for_devices()
    
    if devices:
        print("Available Bluetooth devices:")
        for i, device in enumerate(devices):
            print(f"{i}: {device.name} ({device.address})")

        device_number = int(input("Enter the number of the device you want to connect to: "))
        if 0 <= device_number < len(devices):
            await monitor.connect_to_device(devices[device_number])
            
            while True:
                action = input("Enter '1' to start workout, '2' to end workout, '3' to exit: ")
                if action == '1':
                    await monitor.start_workout()
                elif action == '2':
                    await monitor.end_workout()
                elif action == '3':
                    if monitor.client:
                        await monitor.client.disconnect()
                    break
                else:
                    print("Invalid input. Please try again.")
        else:
            print("Invalid device number")
    else:
        print("No Bluetooth devices found")

if __name__ == "__main__":
    asyncio.run(main())
