# Edit mode
import board
import terminalio
import displayio
from adafruit_display_text import label
import adafruit_ili9341

# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.D6
tft_dc = board.D9

display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=board.D5
)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)

#-----------------------------------
# Initialize and draw heads up

display_group = displayio.Group()
display.show(display_group)

color_bitmap = displayio.Bitmap(320, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000

bg_matte = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
display_group.append(bg_matte) #[0]

display_group.append(label.Label(terminalio.FONT, scale=1, x=2, y=8, text="The LavenderPad is in edit mode.\nThe device should appear as a drive on your computer.\nYou may edit macros/configuration files.\n\nTo exit edit mode and restart the device,\npress the Reset button.")) #[1]

while True:
    pass
