# main.py
import asyncio
from scanner import find_device_by_name
from connector import HeartRateMonitor
from workout_manager import WorkoutManager
import os
import json
from datetime import datetime
import csv

TARGET_DEVICE_NAME = "M7-08252"

async def main():
    manager = WorkoutManager()
    monitor = HeartRateMonitor(manager)
    device = await find_device_by_name(TARGET_DEVICE_NAME)
    
    if device:
        await monitor.connect_to_device(device)
        
        while True:
            action = input("Enter '1' to start workout, '2' to end workout, '3' to generate JSON, '4' to exit: ")
            if action == '1':
                manager.start_workout()
            elif action == '2':
                await monitor.stop_notifications()
                duration_str, filename_suffix, heart_rates = manager.end_workout()
                filename = f"workout_data/workout_{filename_suffix}.csv"
                print(f"Data logged to {filename}")
            elif action == '3':
                generate_json_log()
            elif action == '4':
                await monitor.stop_notifications()
                break
            else:
                print("Invalid input. Please try again.")
    else:
        print(f"Device {TARGET_DEVICE_NAME} not found")

def generate_json_log():
    json_filename = "workout_data/workouts_log.json"
    workouts = []

    if os.path.exists(json_filename):
        with open(json_filename, 'r') as file:
            data = json.load(file)
            workouts = data.get("workouts", [])

    for csv_file in os.listdir("workout_data"):
        if csv_file.endswith(".csv") and not any(workout['filename'] == csv_file for workout in workouts):
            with open(os.path.join("workout_data", csv_file), 'r') as file:
                reader = csv.DictReader(file)
                heart_rates = [int(row['HeartRate']) for row in reader]
                
                if heart_rates:
                    max_hr = max(heart_rates)
                    min_hr = min(heart_rates)
                    avg_hr = sum(heart_rates) / len(heart_rates)

                    # Extract date and time from filename
                    parts = csv_file.split('_')
                    date = parts[1]
                    time = parts[2].split('.')[0]
                    date_str = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
                    time_str = f"{time[:2]}:{time[2:4]}:{time[4:6]}"

                    workout_data = {
                        "date": date_str,
                        "filename": csv_file,
                        "total_time": time_str,
                        "max_hr": max_hr,
                        "min_hr": min_hr,
                        "avg_hr": avg_hr
                    }
                    workouts.append(workout_data)
    
    with open(json_filename, 'w') as file:
        json.dump({"workouts": workouts}, file, indent=4)
    print(f"Workout data logged to {json_filename}")


if __name__ == "__main__":
    asyncio.run(main())
