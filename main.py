import time
import PIL.Image
from PIL import ImageTk
from tkinter import *
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
            # Real clicking speed is too slow compared to given intervals (best - 9.2cps during 10 seconds test, 100ms)
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


def theme():
    """Changes background color depending on theme_state boolean"""
    global theme_state
    theme_state ^= True
    if theme_state:
        theme_btn.config(image=sun_img, bg='#F3F3EF', activebackground='#F3F3EF')
        frame.config(bg='#F3F3EF')
        for label in [time_label, key_label, start_label]:
            label.config(bg='#F3F3EF', fg='black')
    else:
        theme_btn.config(image=moon_img, bg='#253B52', activebackground='#253B52')
        frame.config(bg='#253B52')
        for label in [time_label, key_label, start_label]:
            label.config(bg='#253B52', fg='#F3F3EF')


"""Main window configuration"""
root = Tk()
root.title('Simple autoclicker')  # Set the title
root.resizable(False, False)  # Set width and height to non-resizable
frame = Frame(root, padx=5, pady=5, bg='#F3F3EF')
frame.grid()

"""Button to click configuration label and entry box"""
key_label = Label(frame, text='Button to click', bg='#F3F3EF', fg='black')
key_entry = Entry(frame, width=10, justify='center')
key_entry.insert(0, 'left')  # Default button to click
key_entry.config(state=DISABLED)  # Temporary
# TODO: Add the possibility to change the button/key to click

"""Time configuration label and entry box"""
time_reg = root.register(time_callback)
time_label = Label(frame, text='Time config (in ms)', bg='#F3F3EF', fg='black')
time_entry = Entry(frame, width=10, justify='center', validate='key', validatecommand=(time_reg, '%P'))
time_entry.insert(0, '100')  # Default time interval

"""Start/Stop configuration label and entry box"""
start_label = Label(frame, text='Start/Stop hotkey', bg='#F3F3EF', fg='black')
start_entry = Entry(frame, width=5, justify='center')
start_entry.insert(0, 'F4')  # Default hotkey for Start/Stop
start_entry.config(state=DISABLED)  # Temporary
# TODO: Add the possibility to change Start/Stop hotkey

"""Start/Stop mechanism"""
state = False  # True for ON, False for OFF
state_btn = Button(frame, text='Start', command=toggle, width=10)  # Start/Stop button
keyboard.on_press(keypress_callback)  # Start/Stop hotkey

"""Theme changing"""
theme_state = True  # True for light, False for dark
moon_img = ImageTk.PhotoImage(PIL.Image.open('moon.png').resize(size=(20, 25)))
sun_img = ImageTk.PhotoImage(PIL.Image.open('sun.png').resize(size=(25, 25)))
theme_btn = Button(frame, image=sun_img, command=theme, bg='#F3F3EF', activebackground='#F3F3EF', bd=0)

"""Widgets align"""
key_label.grid(column=0, row=0, padx=(30, 0))
key_entry.grid(column=0, row=1, pady=20, padx=(30, 0))
time_label.grid(column=1, row=0, padx=(30, 30))
time_entry.grid(column=1, row=1, pady=20, padx=(30, 30))
start_label.grid(column=2, row=0, padx=(0, 30))
start_entry.grid(column=2, row=1, pady=20, padx=(0, 30))
state_btn.grid(column=2, row=2, sticky='E')
theme_btn.grid(column=0, row=2, sticky='W')

root.mainloop()
