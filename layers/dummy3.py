# MACROPAD Hotkeys example: Firefox web browser for Linux

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
empty = (0x000000, '', [])

layer = {                       # REQUIRED dict, must be named 'layer'
    'name' : 'Dummy', # Application name
    'macros' : [              # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0xFF0000, 'See, n', [Keycode.CONTROL, '[']),
        (0xFF0000, 'ormall', [Keycode.CONTROL, ']']),
        (0xFF0000, 'y if y', [Keycode.SHIFT, ' ']),      # Scroll up
        (0xFF0000, 'ou go ', [Keycode.CONTROL, Keycode.SHIFT, Keycode.TAB]),
        # 2nd row ----------
        (0xFF0000, '1-on-1', [Keycode.CONTROL, Keycode.TAB]),
        (0xFF0000, ' with ', ' '),                     # Scroll down
        (0xFF0000, 'anothe', [Keycode.CONTROL, 'r']),
        (0xFF0000, 'r', [Keycode.CONTROL, 'h']),
        # 3rd row ----------
        (0xFF0000, 'wrestl', [Keycode.CONTROL, Keycode.SHIFT, 'p']),
        (0xFF0000, 'er, yo', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                           'www.adafruit.com\n']), # adafruit.com in a new tab
        (0xFF0000, 'u got ', [Keycode.F12]),     # dev mode
        (0xFF0000, 'a', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                            'digikey.com\n']),     # digikey in a new tab
    ]
}
