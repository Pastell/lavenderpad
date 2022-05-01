# Macro Layer: Function, keypad of F13 through F24

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
empty = (0x000000, '', [])

layer = {                       # REQUIRED dict, must be named 'layer'
    'name' : 'Function', # Application name
    'macros' : [              # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x000000, 'F21', [Keycode.F21]),
        (0x000000, 'F22', [Keycode.F22]),
        (0x000000, 'F23', [Keycode.F23]),
        (0x000000, 'F24', [Keycode.F24]),
        # 2nd row ----------
        (0x000000, 'F17', [Keycode.F17]),
        (0x000000, 'F18', [Keycode.F18]),
        (0x000000, 'F19', [Keycode.F19]),
        (0x000000, 'F20', [Keycode.F20]),
        # 3rd row ----------
        (0x000000, 'F13', [Keycode.F13]),
        (0x000000, 'F14', [Keycode.F14]),
        (0x000000, 'F15', [Keycode.F15]),
        (0x000000, 'F16', [Keycode.F16]),
    ]
}
