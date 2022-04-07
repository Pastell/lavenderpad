# MACROPAD Hotkeys example: Firefox web browser for Linux

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
empty = (0x000000, '', [])

layer = {                       # REQUIRED dict, must be named 'layer'
    'name' : 'LED', # Application name
    'macros' : [              # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0xFF0000, '', ''),
        (0xFF0000, '', ''),
        (0xFF0000, '', ''),      # Scroll up
        (0xFF0000, '', ''),
        # 2nd row ----------
        (0xFF0000, '', ''),
        (0xFF0000, '', ''),                     # Scroll down
        (0xFF0000, '', ''),
        (0xFF0000, '', ''),
        # 3rd row ----------
        (0xFF0000, '', ''),
        (0xFF0000, '', ''),
        (0xFF0000, '', ''),     # dev mode
        (0xFF0000, '', ''),     # digikey in a new tab
    ]
}
