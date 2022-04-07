# MACROPAD Hotkeys example: Firefox web browser for Linux

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
empty = (0x000000, '', [])

layer = {                       # REQUIRED dict, must be named 'layer'
    'name' : 'Firefox', # Application name
    'macros' : [              # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x004000, '< Back', [Keycode.ALT, Keycode.LEFT_ARROW]),
        (0x004000, 'Fwd >', [Keycode.ALT, Keycode.RIGHT_ARROW]),
        (0x400000, 'Up', [Keycode.SHIFT, ' ']),      # Scroll up
        (0x000040, 'Reload', [Keycode.CONTROL, 'r']),
        # 2nd row ----------
        (0x202000, '< Tab', [Keycode.CONTROL, Keycode.SHIFT, Keycode.TAB]),
        (0x202000, 'Tab >', [Keycode.CONTROL, Keycode.TAB]),
        (0x400000, 'Down', ' '),                     # Scroll down
        (0x000040, 'NewTab', [Keycode.CONTROL, 't']),
        # 3rd row ----------
        (0x101010, 'RckRll', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                           'https://youtu.be/zL19uMsnpSU',
                           Keycode.RETURN, -Keycode.RETURN, 1.0, Keycode.SPACE, -Keycode.SPACE]), # adafruit.com in a new tab
        (0x101010, 'BrckRl', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                           'https://youtu.be/65I0HNvTDH4',
                           Keycode.RETURN, -Keycode.RETURN, 1.0, Keycode.SPACE, -Keycode.SPACE]), # adafruit.com in a new tab
        (0x101010, 'MdvlRl', [Keycode.CONTROL, 't', -Keycode.CONTROL,
                           'https://youtu.be/YxjY_YTksKM',
                           Keycode.RETURN, -Keycode.RETURN, 1.0, Keycode.SPACE, -Keycode.SPACE]), # adafruit.com in a new tab
        (0x000040, 'DvMode', [Keycode.F12]),     # dev mode
    ]
}
