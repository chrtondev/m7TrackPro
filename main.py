# main.py
import asyncio
from scanner import find_device_by_name
from connector import HeartRateMonitor
from workout_manager import WorkoutManager
import os

TARGET_DEVICE_NAME = "M7-08252"

async def main():
    manager = WorkoutManager()
    monitor = HeartRateMonitor(manager)
    device = await find_device_by_name(TARGET_DEVICE_NAME)
    
    if device:
        await monitor.connect_to_device(device)
        
        while True:
            action = input("Enter '1' to start workout, '2' to end workout, '3' to exit: ")
            if action == '1':
                manager.start_workout()
            elif action == '2':
                data, duration = manager.end_workout()
                
                # Generate filename
                filename = f"workout_data/workout_{manager.start_time.strftime('%Y-%m-%d_%H%M%S')}.csv"
                
                # Ensure the workout_data directory exists
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                
                # Log data to CSV
                manager.log_to_csv(filename, data)
                
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
