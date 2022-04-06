# MACROPAD Hotkeys example: Firefox web browser for Linux

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
empty = (0x000000, '', [])

layer = {                       # REQUIRED dict, must be named 'layer'
    'name' : 'Dummy', # Application name
    'macros' : [              # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0xFF0000, '50/50 ', [Keycode.CONTROL, '[']),
        (0xFF0000, 'chance', [Keycode.CONTROL, ']']),
        (0xFF0000, 'of win', [Keycode.SHIFT, ' ']),      # Scroll up
        (0xFF0000, 'ning. ', [Keycode.CONTROL, Keycode.SHIFT, Keycode.TAB]),
        # 2nd row ----------
        (0xFF0000, 'But Im', [Keycode.CONTROL, Keycode.TAB]),
        (0xFF0000, 'a gene', ' '),                     # Scroll down
        (0xFF0000, 'tic fr', [Keycode.CONTROL, 'r']),
        (0xFF0000, 'eak,  ', [Keycode.CONTROL, 'h']),
        # 3rd row ----------
        (0xFF0000, 'and Im', [Keycode.CONTROL, Keycode.SHIFT, 'p']),
        (0xFF0000, 'not no', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                           'www.adafruit.com\n']), # adafruit.com in a new tab
        (0xFF0000, 'rmal! ', [Keycode.F12]),     # dev mode
        (0xFF0000, '', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                            'digikey.com\n']),     # digikey in a new tab
    ]
}
