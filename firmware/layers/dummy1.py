# MACROPAD Hotkeys example: Firefox web browser for Linux

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
empty = (0x000000, '', [])

layer = {                       # REQUIRED dict, must be named 'layer'
    'name' : 'Dummy1', # Application name
    'macros' : [              # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0xFF0000, 'You kn', [Keycode.CONTROL, '[']),
        (0xFF0000, 'ow the', [Keycode.CONTROL, ']']),
        (0xFF0000, 'y say ', [Keycode.SHIFT, ' ']),      # Scroll up
        (0xFF0000, 'that  ', [Keycode.CONTROL, Keycode.SHIFT, Keycode.TAB]),
        # 2nd row ----------
        (0xFF0000, 'all me', [Keycode.CONTROL, Keycode.TAB]),
        (0xFF0000, 'n are ', ' '),                     # Scroll down
        (0xFF0000, 'create', [Keycode.CONTROL, 'r']),
        (0xFF0000, 'd     ', [Keycode.CONTROL, 'h']),
        # 3rd row ----------
        (0xFF0000, 'equal,', [Keycode.CONTROL, Keycode.SHIFT, 'p']),
        (0xFF0000, 'but yo', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                           'www.adafruit.com\n']), # adafruit.com in a new tab
        (0xFF0000, 'u look', [Keycode.F12]),     # dev mode
        (0xFF0000, ' at me', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                            'digikey.com\n']),     # digikey in a new tab
    ]
}
