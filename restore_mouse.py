import pyautogui
import keyboard
import pickle
import datetime

def store_position(index):
    position = pyautogui.position()
    now = datetime.datetime.now()
    print(f"Position {index} stored at {now}: {position}")
    with open(f"stored_position_{index}.pickle", "wb") as f:
        pickle.dump((position, now), f)
    return position

def overwrite_position(index):
    position = pyautogui.position()
    now = datetime.datetime.now()
    print(f"Position {index} overwritten at {now}: {position}")
    with open(f"stored_position_{index}.pickle", "wb") as f:
        pickle.dump((position, now), f)
    return position

def revert_position(index):
    try:
        with open(f"stored_position_{index}.pickle", "rb") as f:
            position, stored_time = pickle.load(f)
        pyautogui.moveTo(position)
        print(f"Reverted to position {index} stored at {stored_time}: {position}")
    except FileNotFoundError:
        print(f"Position {index} not found")

def manual_store_position():
    index = int(input("Enter index (1-3): "))
    if index in [1, 3, 5]:
        x = int(input("Enter X coordinate: "))
        y = int(input("Enter Y coordinate: "))
        position = (x, y)
        if keyboard.is_pressed(f'F{index}'):
            overwrite_position(index)
        else:
            with open(f"stored_position_{index}.pickle", "wb") as f:
                pickle.dump((position, datetime.datetime.now()), f)
            print(f"Position {index} stored manually at {datetime.datetime.now()}: {position}")
    else:
        print("Invalid index. Only F1, F3, and F5 are allowed.")

def manual_revert_position():
    index = int(input("Enter index (1-3): "))
    revert_position(index)

def check_stored_positions():
    stored_positions = {}
    for i in [1, 2, 3, 4, 5, 6]:
        try:
            with open(f"stored_position_{i}.pickle", "rb") as f:
                position, stored_time = pickle.load(f)
            stored_positions[i] = (position, stored_time)
        except FileNotFoundError:
            pass
    if stored_positions:
        print("Stored positions:")
        for index, (position, stored_time) in stored_positions.items():
            print(f"{index}: {position} stored at {stored_time}")
    else:
        print("No stored positions found")

print("Welcome! F1, F3, and F5 are used for storing positions. F2, F4, and F6 are used for reverting positions.")
check_stored_positions()

keyboard.add_hotkey('Ctrl + Alt + F1', lambda: store_position(1))
keyboard.add_hotkey('Ctrl + Alt + F3', lambda: store_position(2))
keyboard.add_hotkey('Ctrl + Alt + F5', lambda: store_position(3))
keyboard.add_hotkey('Ctrl + Alt + F2', lambda: revert_position(1))
keyboard.add_hotkey('Ctrl + Alt + F4', lambda: revert_position(2))
keyboard.add_hotkey('Ctrl + Alt + F6', lambda: revert_position(3))

keyboard.add_hotkey('Ctrl + Alt + F7', manual_store_position)
keyboard.add_hotkey('Ctrl + Alt + F8', manual_revert_position)

# Add an exit hotkey
keyboard.add_hotkey('Ctrl + Alt + Q', lambda: keyboard.unhook_all())

keyboard.wait()
