# workout_manager.py
import csv
from datetime import datetime
import os

class WorkoutManager:
    def __init__(self):
        self.start_time = None
        self.csv_file = None
        self.csv_writer = None
        self.workout_active = False

    def start_workout(self):
        self.start_time = datetime.now()
        filename = f"workout_data/workout_{self.start_time.strftime('%Y-%m-%d_%H%M%S')}.csv"
        
        # Ensure the workout_data directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Open the CSV file for appending
        self.csv_file = open(filename, 'a', newline='')
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=["Time", "HeartRate"])
        self.csv_writer.writeheader()
        self.workout_active = True
        print(f"Workout started at {self.start_time}. Logging to {filename}")

    def log_data_point(self, heart_rate):
        if self.workout_active and self.csv_writer:
            elapsed_time = datetime.now() - self.start_time
            timestamp = str(elapsed_time).split('.')[0] + '.' + str(elapsed_time.microseconds // 1000).zfill(3)
            print(f"Logging data point: Time={timestamp}, HeartRate={heart_rate}")  # Debug print
            self.csv_writer.writerow({"Time": timestamp, "HeartRate": heart_rate})
            self.csv_file.flush()  # Ensure data is written to disk
            print(f"Logged heart rate: {heart_rate} bpm at {timestamp}")

    def end_workout(self):
        self.workout_active = False
        end_time = datetime.now()
        duration = end_time - self.start_time
        print(f"Workout ended. Duration: {duration}")
        
        # Close the CSV file
        if self.csv_file:
            self.csv_file.close()
        
        return duration