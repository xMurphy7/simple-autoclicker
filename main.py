import time
from tkinter import *
from tkinter import ttk
from threading import Thread
import mouse
import keyboard
import logging

logging.basicConfig(filename='main.log', filemode='w', level=logging.DEBUG)


def autoclick(click_key: str, time_ms: int):
    """This function executes clicking the given button in specified time intervals.
    :param click_key: Key to click
    :param time_ms: Time given in milliseconds
    """
    interval = time_ms / 1000  # time.sleep() uses seconds, so you need to divide input by 1000
    if click_key == 'left':
        while state:
            # Real clicking speed is too slow compared to given intervals
            mouse.click(LEFT)
            time.sleep(interval)
            # TODO: Loop doesn't end immediately after stop because thread has to wait until interval time passes


# TODO: Change button state to avoid auto-stopping the clicker
def toggle():
    """Function that runs Start/Stop mechanism. When button or hotkey is pressed, this function changes state to
    True/False. If state is True, it calls autoclick()."""
    global state
    time_ms = time_entry.get()
    click_key = key_entry.get()
    if time_ms != '' and not time_ms.startswith('0'):
        state ^= True
        time_ms = int(time_ms)
        if state:
            state_btn.config(text='Stop')  # Change text on the button to 'Stop'
            t = Thread(target=autoclick, args=[str(click_key), time_ms])
            t.start()
        elif state is False:
            state_btn.config(text='Start')  # Change text on the button to 'Start'
        logging.info(state)


def time_callback(time_input):
    """Callback used to validate time input in the entry box"""
    if (time_input.isdigit() or time_input == '') and len(time_input) <= 10:
        return True
    else:
        return False


def keypress_callback(event):
    """Callback used to run toggle() function on pressing a key"""
    start_key = start_entry.get().lower()
    if event.name == start_key:
        toggle()


# TODO: Light/Dark Theme
def theme():
    pass


"""Main window configuration"""
root = Tk()
root.title('Simple autoclicker')  # Set the title
root.resizable(False, False)  # Set width and height to non-resizable
frame = ttk.Frame(root, padding=10)
frame.grid()

"""Button to click configuration label and entry box"""
key_label = ttk.Label(frame, text='Button to click')
key_entry = ttk.Entry(frame, width=10, justify='center')
key_entry.insert(END, 'left')
key_entry.config(state=DISABLED)  # Temporary
# TODO: Add the possibility to change the button/key to click

"""Time configuration label and entry box"""
time_reg = root.register(time_callback)
time_label = ttk.Label(frame, text='Time config (in ms)')
time_entry = ttk.Entry(frame, width=10, justify='center', validate='key', validatecommand=(time_reg, '%P'))
time_entry.insert(END, '100')

"""Start/Stop configuration label and entry box"""
start_label = ttk.Label(frame, text='Start/Stop hotkey')
start_entry = ttk.Entry(frame, width=5, justify='center')
start_entry.insert(END, 'F4')
start_entry.config(state=DISABLED)  # Temporary
# TODO: Add the possibility to change Start/Stop hotkey

"""Start/Stop mechanism"""
state = False
state_btn = ttk.Button(frame, text='Start', command=toggle)  # Start/Stop button
keyboard.on_press(keypress_callback)  # Start/Stop hotkey

"""Widgets align"""
key_label.grid(column=0, row=0)
key_entry.grid(column=0, row=1)
time_label.grid(column=1, row=0)
time_entry.grid(column=1, row=1)
start_label.grid(column=2, row=0)
start_entry.grid(column=2, row=1)
state_btn.grid(column=1, row=2)

root.mainloop()
