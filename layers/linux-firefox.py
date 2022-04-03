# MACROPAD Hotkeys example: Firefox web browser for Linux

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
empty = (0x000000, '', [])

layer = {                       # REQUIRED dict, must be named 'layer'
    'name' : 'Linux Firefox', # Application name
    'macros' : [              # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x004000, '< Back', [Keycode.CONTROL, '[']),
        (0x004000, 'Fwd >', [Keycode.CONTROL, ']']),
        (0x400000, 'Up', [Keycode.SHIFT, ' ']),      # Scroll up
        (0x202000, '< Tab', [Keycode.CONTROL, Keycode.SHIFT, Keycode.TAB]),
        # 2nd row ----------
        (0x202000, 'Tab >', [Keycode.CONTROL, Keycode.TAB]),
        (0x400000, 'Down', ' '),                     # Scroll down
        (0x000040, 'Reload', [Keycode.CONTROL, 'r']),
        (0x000040, 'Home', [Keycode.CONTROL, 'h']),
        # 3rd row ----------
        (0x000040, 'Priv', [Keycode.CONTROL, Keycode.SHIFT, 'p']),
        (0x101010, 'Ada', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                           'www.adafruit.com\n']), # adafruit.com in a new tab
        (0x000040, 'DevMod', [Keycode.F12]),     # dev mode
        (0x101010, 'Digi', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                            'digikey.com\n']),     # digikey in a new tab
    ]
}
