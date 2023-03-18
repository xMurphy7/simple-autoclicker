# Simple autoclicker
This is my first bigger project made in Python. It is a simple autoclicker that can be used in games, for example.

## Features
- Possibility to use left/middle/right mouse button for clicking
- Possibility to change the time interval between the clicks
- Possibility to use and change the start/stop hotkey
- Light/dark theme

## Known bugs
- If you stop and start clicking again quickly during the pause between the clicks, an additional thread will be created and the number of clicks will double.
- If you move your cursor through a window's close button and then to another window during really small intervals (like 10ms), the autoclicker may register additional clicks even after the window has been closed.
