# MACROPAD Hotkeys example: Firefox web browser for Linux

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
empty = (0x000000, '', [])

layer = {                       # REQUIRED dict, must be named 'layer'
    'name' : 'Dummy', # Application name
    'macros' : [              # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0xFF0000, 'your c', [Keycode.CONTROL, '[']),
        (0xFF0000, 'hances', [Keycode.CONTROL, ']']),
        (0xFF0000, ' of wi', [Keycode.SHIFT, ' ']),      # Scroll up
        (0xFF0000, 'nning ', [Keycode.CONTROL, Keycode.SHIFT, Keycode.TAB]),
        # 2nd row ----------
        (0xFF0000, 'drasti', [Keycode.CONTROL, Keycode.TAB]),
        (0xFF0000, 'c go d', ' '),                     # Scroll down
        (0xFF0000, 'own. S', [Keycode.CONTROL, 'r']),
        (0xFF0000, 'ee the', [Keycode.CONTROL, 'h']),
        # 3rd row ----------
        (0xFF0000, '3-way ', [Keycode.CONTROL, Keycode.SHIFT, 'p']),
        (0xFF0000, 'at Sac', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                           'www.adafruit.com\n']), # adafruit.com in a new tab
        (0xFF0000, 'rifice', [Keycode.F12]),     # dev mode
        (0xFF0000, ', you', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                            'digikey.com\n']),     # digikey in a new tab
    ]
}
