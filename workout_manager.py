# i am in workout_manager.py
from datetime import datetime

class WorkoutManager:
    def __init__(self):
        self.data = []
        self.start_time = None

    def start_workout(self):
        self.data = []
        self.start_time = datetime.now()
        print("Workout started...")

    def end_workout(self):
        end_time = datetime.now()
        duration = end_time - self.start_time
        print(f"Workout ended. Duration: {duration}")
        for timestamp, heart_rate in self.data:
            print(f"{timestamp}: {heart_rate} bpm")
        return self.data
