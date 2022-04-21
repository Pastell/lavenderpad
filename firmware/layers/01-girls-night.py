# MACROPAD Hotkeys example: Firefox web browser for Linux

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
empty = (0x000000, '', [])

layer = {                       # REQUIRED dict, must be named 'layer'
    'name' : 'Girls Night', # Application name
    'macros' : [              # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x1D919B, 'Girls ', ['https://cdn.discordapp.com/attachments/924557055036129311/965798630848086066/GIRLS_NIGHT.png', Keycode.RETURN]),
        (0x1D919B, 'Night ', ['https://cdn.discordapp.com/attachments/924557055036129311/965798630848086066/GIRLS_NIGHT.png', Keycode.RETURN]),
        (0x1D919B, 'Girls ', ['https://cdn.discordapp.com/attachments/924557055036129311/965798630848086066/GIRLS_NIGHT.png', Keycode.RETURN]),
        (0x1D919B, 'Night ', ['https://cdn.discordapp.com/attachments/924557055036129311/965798630848086066/GIRLS_NIGHT.png', Keycode.RETURN]),
        # 2nd row ----------
        (0x1D919B, 'Girls ', ['https://cdn.discordapp.com/attachments/924557055036129311/965798630848086066/GIRLS_NIGHT.png', Keycode.RETURN]),
        (0x1D919B, 'Night ', ['https://cdn.discordapp.com/attachments/924557055036129311/965798630848086066/GIRLS_NIGHT.png', Keycode.RETURN]),
        (0x1D919B, 'Girls ', ['https://cdn.discordapp.com/attachments/924557055036129311/965798630848086066/GIRLS_NIGHT.png', Keycode.RETURN]),
        (0x1D919B, 'Night ', ['https://cdn.discordapp.com/attachments/924557055036129311/965798630848086066/GIRLS_NIGHT.png', Keycode.RETURN]),
        # 3rd row ----------
        (0x1D919B, 'Girls ', ['https://cdn.discordapp.com/attachments/924557055036129311/965798630848086066/GIRLS_NIGHT.png', Keycode.RETURN]),
        (0x1D919B, 'Night ', ['https://cdn.discordapp.com/attachments/924557055036129311/965798630848086066/GIRLS_NIGHT.png', Keycode.RETURN]),
        (0x1D919B, 'Girls ', ['https://cdn.discordapp.com/attachments/924557055036129311/965798630848086066/GIRLS_NIGHT.png', Keycode.RETURN]),
        (0x1D919B, 'Night ', ['https://cdn.discordapp.com/attachments/924557055036129311/965798630848086066/GIRLS_NIGHT.png', Keycode.RETURN]),
    ]
}
