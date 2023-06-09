import threading
import time
import PIL.Image
from PIL import ImageTk
from tkinter import *
from threading import Thread
import mouse
import keyboard
import logging
import sys,os

logging.basicConfig(level=logging.DEBUG)


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def autoclick(click_key: str, time_ms: int):
    """This function executes clicking the given button in specified time intervals.
    :param click_key: Key to click
    :param time_ms: Time given in milliseconds
    """
    logging.info('Started autoclick thread')
    interval = time_ms / 1000  # time.sleep() uses seconds, so you need to divide input by 1000
    click_key = click_key.lower()
    while state:
        mouse.click(button=click_key)
        time.sleep(interval)


def disable_btn():
    """Disable start/stop button for 1 second to prevent instant stopping"""
    state_btn.config(state=DISABLED)
    time.sleep(1)
    state_btn.config(state=NORMAL)


def toggle():
    """Function that runs Start/Stop mechanism. When button or hotkey is pressed, this function changes state to
    True/False. If state is True, it calls autoclick()."""
    global state
    time_ms = time_entry.get()
    click_key = cur_key.get()
    if time_ms != '' and not time_ms.startswith('0'):
        logging.info(f'Current threads: {threading.enumerate()}')
        state ^= True
        time_ms = int(time_ms)
        if state:
            logging.info(f'State = {state}')
            state_btn.config(text='Stop')  # Change text on the button to 'Stop'
            toggle_thread = Thread(target=autoclick, args=[click_key, time_ms], daemon=True)
            toggle_thread.start()
            disable_btn_thread = Thread(target=disable_btn, daemon=True)
            disable_btn_thread.start()
        elif state is False:
            logging.info(f'State = {state}')
            state_btn.config(text='Start')  # Change text on the button to 'Start'


def time_callback(time_input):
    """Callback used to validate time input in the entry box"""
    if (time_input.isdigit() or time_input == '') and len(time_input) <= 10:
        return True
    else:
        return False


def keypress_callback(event):
    """Callback used to run toggle() function on pressing a key"""
    hotkey = str(start_config['text'])
    if event.name == hotkey.lower():
        toggle()


def change_hotkey():
    """Create the thread that awaits for keyboard event and changes the hotkey for Start/Stop"""

    def read_hotkey():
        """Wait for a keyboard event and change the hotkey"""
        hotkey = str(keyboard.read_key())
        start_config['text'] = hotkey

    start_config['text'] = '<INSERT>'
    start_thread = Thread(target=read_hotkey, daemon=True)
    start_thread.start()


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
            label.config(bg='#253B52', fg='white')


"""Main window configuration"""
root = Tk()
root.title('Simple autoclicker')  # Set the title
root.resizable(False, False)  # Set width and height to non-resizable
frame = Frame(root, padx=5, pady=5, bg='#F3F3EF')
frame.grid()

"""Button to click configuration label and option menu"""
key_label = Label(frame, text='Button to click', bg='#F3F3EF', fg='black')
cur_key = StringVar(value='Left')
key_config = OptionMenu(frame, cur_key, 'Left', 'Right', 'Middle')
key_config.config(width=6, highlightthickness=0)

"""Time configuration label and entry box"""
time_reg = root.register(time_callback)
time_label = Label(frame, text='Time config (in ms)', bg='#F3F3EF', fg='black')
time_entry = Entry(frame, width=10, justify='center', validate='key', validatecommand=(time_reg, '%P'))
time_entry.insert(0, '100')  # Default time interval

"""Start/Stop configuration label and button"""
start_label = Label(frame, text='Start/Stop hotkey', bg='#F3F3EF', fg='black')
start_config = Button(frame, width=8, justify='center', text='f4', command=change_hotkey)

"""Start/Stop mechanism"""
state = False  # True for ON, False for OFF
state_btn = Button(frame, text='Start', command=toggle, width=10)  # Start/Stop button
keyboard.on_press(keypress_callback)  # Start/Stop hotkey

"""Theme changing"""
theme_state = True  # True for light, False for dark
moon_img = ImageTk.PhotoImage(PIL.Image.open(resource_path('moon.png')).resize(size=(20, 25)))
sun_img = ImageTk.PhotoImage(PIL.Image.open(resource_path('sun.png')).resize(size=(25, 25)))
theme_btn = Button(frame, image=sun_img, command=theme, bg='#F3F3EF', activebackground='#F3F3EF', bd=0)

"""Widgets align"""
key_label.grid(column=0, row=0, padx=(30, 0))
key_config.grid(column=0, row=1, pady=20, padx=(30, 0))
time_label.grid(column=1, row=0, padx=(30, 30))
time_entry.grid(column=1, row=1, pady=20, padx=(30, 30))
start_label.grid(column=2, row=0, padx=(0, 30))
start_config.grid(column=2, row=1, pady=20, padx=(0, 30))
state_btn.grid(column=2, row=2, sticky='E')
theme_btn.grid(column=0, row=2, sticky='W')

root.mainloop()
