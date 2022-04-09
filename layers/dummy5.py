# MACROPAD Hotkeys example: Firefox web browser for Linux

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
empty = (0x000000, '', [])

layer = {                       # REQUIRED dict, must be named 'layer'
    'name' : 'Dummy', # Application name
    'macros' : [              # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0xFF0000, 'So you', [Keycode.CONTROL, '[']),
        (0xFF0000, 'got a ', [Keycode.CONTROL, ']']),
        (0xFF0000, '25% at', [Keycode.SHIFT, ' ']),      # Scroll up
        (0xFF0000, 'BEST  ', [Keycode.CONTROL, Keycode.SHIFT, Keycode.TAB]),
        # 2nd row ----------
        (0xFF0000, 'at bea', [Keycode.CONTROL, Keycode.TAB]),
        (0xFF0000, 't me. ', ' '),                     # Scroll down
        (0xFF0000, 'Then y', [Keycode.CONTROL, 'r']),
        (0xFF0000, 'ou add', [Keycode.CONTROL, 'h']),
        # 3rd row ----------
        (0xFF0000, 'Kurt A', [Keycode.CONTROL, Keycode.SHIFT, 'p']),
        (0xFF0000, 'ngle t', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                           'www.adafruit.com\n']), # adafruit.com in a new tab
        (0xFF0000, 'o the ', [Keycode.F12]),     # dev mode
        (0xFF0000, 'mix,', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                            'digikey.com\n']),     # digikey in a new tab
    ]
}
