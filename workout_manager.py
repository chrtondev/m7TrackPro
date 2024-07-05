# workout_manager.py
import csv
from datetime import datetime
import os

class WorkoutManager:
    def __init__(self):
        self.data = []
        self.start_time = None

    def start_workout(self):
        self.data = []
        self.start_time = datetime.now()
        print("Workout started...")

    def log_data_point(self, timestamp, heart_rate):
        self.data.append((timestamp, heart_rate))


    def end_workout(self):
        end_time = datetime.now()
        duration = end_time - self.start_time
        print(f"Workout ended. Duration: {duration}")
        for timestamp, heart_rate in self.data:
            print(f"{timestamp}: {heart_rate} bpm")
        return self.data, duration

    def log_to_csv(self, filename, data):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time', 'HeartRate'])
            writer.writerows(data)
        print(f"Data logged to {filename}")
