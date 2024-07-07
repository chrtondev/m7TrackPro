# workout_manager.py
import csv
import json
from datetime import datetime
import os

class WorkoutManager:
    def __init__(self):
        self.start_time = None
        self.csv_file = None
        self.csv_writer = None
        self.workout_active = False
        self.data_point_index = 0
        self.heart_rates = []

    def start_workout(self):
        self.start_time = datetime.now()
        filename = f"workout_data/workout_{self.start_time.strftime('%Y-%m-%d_%H%M%S')}.csv"
        
        # Ensure the workout_data directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Open the CSV file for appending
        self.csv_file = open(filename, 'a', newline='')
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=["Number", "HeartRate"])
        self.csv_writer.writeheader()
        self.workout_active = True
        self.data_point_index = 0
        print(f"Workout started at {self.start_time}. Logging to {filename}")

    def log_data_point(self, heart_rate):
        if self.workout_active and self.csv_writer:
            print(f"Logging data point: Number={self.data_point_index}, HeartRate={heart_rate}")  # Debug print
            self.csv_writer.writerow({"Number": self.data_point_index, "HeartRate": heart_rate})
            self.csv_file.flush()  # Ensure data is written to disk
            print(f"Logged heart rate: {heart_rate} bpm at data point {self.data_point_index}")
            self.data_point_index += 1

    def end_workout(self):
        self.workout_active = False
        end_time = datetime.now()
        duration = end_time - self.start_time
        duration_str = str(duration).split('.')[0]
        print(f"Workout ended. Duration: {duration_str}")
        
        # Close the CSV file
        if self.csv_file:
            self.csv_file.close()
        
        return duration_str, self.start_time.strftime('%Y-%m-%d_%H%M%S'), self.heart_rates