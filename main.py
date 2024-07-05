# i am in main.py
import asyncio
from scanner import find_device_by_name
from connector import HeartRateMonitor
from workout_manager import WorkoutManager

# this can be changed to target other heart rate monitors
TARGET_DEVICE_NAME = "M7-08252"

async def main():
    monitor = HeartRateMonitor()
    manager = WorkoutManager()
    device = await find_device_by_name(TARGET_DEVICE_NAME)
    
    if device:
        await monitor.connect_to_device(device)
        
        while True:
            action = input("Enter '1' to start workout, '2' to end workout, '3' to exit: ")
            if action == '1':
                await manager.start_workout()
            elif action == '2':
                await manager.end_workout()
            elif action == '3':
                if monitor.client:
                    await monitor.client.disconnect()
                break
            else:
                print("Invalid input. Please try again.")
    else:
        print(f"Device {TARGET_DEVICE_NAME} not found")

if __name__ == "__main__":
    asyncio.run(main())
