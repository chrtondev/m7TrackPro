# i am in utils.py
import os

# fucntion to clear the screen (terminal window)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
