# MACROPAD Hotkeys example: Firefox web browser for Linux

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
empty = (0x000000, '', [])

layer = {                       # REQUIRED dict, must be named 'layer'
    'name' : 'Dummy', # Application name
    'macros' : [              # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0xFF0000, 'and yo', [Keycode.CONTROL, '[']),
        (0xFF0000, 'u look', [Keycode.CONTROL, ']']),
        (0xFF0000, ' at Sa', [Keycode.SHIFT, ' ']),      # Scroll up
        (0xFF0000, 'moa', [Keycode.CONTROL, Keycode.SHIFT, Keycode.TAB]),
        # 2nd row ----------
        (0xFF0000, 'Joe an', [Keycode.CONTROL, Keycode.TAB]),
        (0xFF0000, 'd you ', ' '),                     # Scroll down
        (0xFF0000, 'can se', [Keycode.CONTROL, 'r']),
        (0xFF0000, 'e that', [Keycode.CONTROL, 'h']),
        # 3rd row ----------
        (0xFF0000, 'statem', [Keycode.CONTROL, Keycode.SHIFT, 'p']),
        (0xFF0000, 'ent is', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                           'www.adafruit.com\n']), # adafruit.com in a new tab
        (0xFF0000, ' not ', [Keycode.F12]),     # dev mode
        (0xFF0000, 'true.', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                            'digikey.com\n']),     # digikey in a new tab
    ]
}
