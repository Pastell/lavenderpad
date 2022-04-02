# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text. All drawing is done
using native displayio modules.

Pinouts are for the 2.4" TFT FeatherWing or Breakout with a Feather M4 or M0.
"""
import supervisor

timer = supervisor.ticks_ms()
import time
import board
import terminalio
import displayio
from adafruit_display_text import label
import adafruit_ili9341
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
import adafruit_74hc595
import busio
import digitalio
import rotaryio
from adafruit_progressbar.verticalprogressbar import (
    VerticalProgressBar,
    VerticalFillDirection,
)
from adafruit_progressbar.horizontalprogressbar import (
    HorizontalProgressBar,
    HorizontalFillDirection,
)
from adafruit_display_shapes.rect import Rect
import gc
import keypad
import neopixel

# color defs
clr_white = 0xFFFFFF  # Absolute White
clr_lavender = 0xB172C6  # Main UI Lavender
clr_lavender_dark = 0x5D4266  # Darker lavender for backgrounds

sleep_timer = 0
TIME_TO_DIM = 10000 # In whole seconds
TIME_TO_SLEEP = 20000 # In whole seconds
DIM_BRIGHTNESS = 0.01 # Float from 0 to 1

def clamp(num, min_value, max_value):
    num = max(min(num, max_value), min_value)
    return num

# Release any resources currently in use for the displays
displayio.release_displays()

spi = board.SPI()
tft_cs = board.D6
tft_dc = board.D9

display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=board.D5
)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240, backlight_pin=board.D4)

# latch_pin = digitalio.DigitalInOut(board.D5)
# sr = adafruit_74hc595.ShiftRegister74HC595(spi, latch_pin)
# pins = [sr.get_pin(n) for n in range(8)]
# A3 = digitalio.DigitalInOut(board.A3)

# -----------------------------------
# Initialize and draw boot splash

# Initialize and render boot splash display group
boot_splash = displayio.Group()
display.show(boot_splash)

# Draw lavender background matte
color_bitmap = displayio.Bitmap(320, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = clr_lavender

splash_matte = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
boot_splash.append(splash_matte)  # [0]

# Draw 1px white border
boot_splash.append(
    Rect(0, 0, 320, 240, fill=clr_lavender, outline=clr_white, stroke=1)
)  # [1]

# Draw LavenderPad logo
bitmap = displayio.OnDiskBitmap("/images/lavenderpad.bmp")
bitmap_tg = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
bitmap_tg.x = 22
bitmap_tg.y = 105
boot_splash.append(bitmap_tg)  # [2]

# Draw credit label
boot_splash.append(
    label.Label(terminalio.FONT, scale=2, x=240, y=40, text="made by pastellexists")
)  # [3]
boot_splash[3].anchor_point = (0.5, 0.5)
boot_splash[3].anchored_position = (160, 150)

# Draw task label

boot_splash.append(
    label.Label(terminalio.FONT, scale=1, x=240, y=40, text="working . . .")
)  # [4]
boot_splash[4].anchor_point = (0.5, 0.5)
boot_splash[4].anchored_position = (160, 200)


def task_label(text):
    boot_splash[4].text = text
    print(text)


# change task label: boot_splash[4].text = "text . . ."
# -----------------------------------
# Initialize the rendering structure
# Variables initialized in back-to-front rendering order

task_label("Initializing UI groups . . .")


ui_background = displayio.Group()  # Lavender background and white border
ui_macro_grid = displayio.Group()  # Lower half grid representing macros
ui_volume_ind = displayio.Group()  # Top-left vertical volume indicator bars
ui_layer_ind = displayio.Group()  # Plain text layer indicator
ui_layer_popup = displayio.Group()  # Layer selection popup. Design not finalized
ui_volume_popup = displayio.Group()  # Top fourth volume adjustment popup

ui = displayio.Group()  # Initialize UI display group

ui.append(ui_background)
ui.append(ui_macro_grid)
ui.append(ui_volume_ind)
ui.append(ui_layer_ind)
ui.append(ui_layer_popup)
ui.append(ui_volume_popup)

# -----------------------------------
# Render ui_background
task_label("Initializing key interface . . .")

pixels = neopixel.NeoPixel(board.D25, 16, brightness=0.2)
pixels.fill((0, 0, 0))  # Begin with pixels off.

COLUMNS = 4
ROWS = 4

keys = keypad.KeyMatrix(
    row_pins=(board.A1, board.A2, board.A3, board.D24),
    column_pins=(board.D13, board.D12, board.D11, board.D10),
    columns_to_anodes=False,
)


def key_to_pixel_map(key_number):
    row = key_number // COLUMNS
    column = key_number % COLUMNS
    if row % 2 == 1:
        column = COLUMNS - column - 1
    return row * COLUMNS + column

# -----------------------------------
# Render ui_background
task_label("Rendering background . . .")


ui_background.append(
    displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
)  # Background matte [0]
ui_background.append(
    Rect(0, 0, 320, 240, fill=clr_lavender, outline=clr_white, stroke=1)
)  # 1px white border [1]

# -----------------------------------
# Render ui_macro_grid
task_label("Rendering macro grid . . .")


layout = GridLayout(
    x=0,
    y=120,
    width=320,
    height=120,
    grid_size=(4, 3),
    cell_padding=4,
    divider_lines=True,  # divider lines around every cell
)

_labels = []

for row in range(3):
    _labels.append([])
    for col in range(4):
        _labels[row].append(
            label.Label(
                terminalio.FONT,
                scale=2,
                x=0,
                y=0,
                text=str(col) + "x" + str(row) + "___",
            )
        )
        layout.add_content(
            _labels[row][col], grid_position=(col, row), cell_size=(1, 1)
        )
# The grid cells are referenced somewhat counter-intuively as _labels[y][x], as in the first number is row and the second is column

ui_macro_grid.append(layout)

# -----------------------------------
# Render ui_volume_ind
task_label("Rendering mixing HUD . . .")


vol_bars_width = 20

_vol_bars = []
_vol_bars.append(
    VerticalProgressBar(
        (vol_bars_width * 0, 0),
        (20, 120),
        fill_color=clr_lavender_dark,
        bar_color=clr_white,
        direction=VerticalFillDirection.BOTTOM_TO_TOP,
    )
)
_vol_bars.append(
    VerticalProgressBar(
        (vol_bars_width * 1, 0),
        (20, 120),
        fill_color=clr_lavender_dark,
        bar_color=clr_white,
        direction=VerticalFillDirection.BOTTOM_TO_TOP,
    )
)
_vol_bars.append(
    VerticalProgressBar(
        (vol_bars_width * 2, 0),
        (20, 120),
        fill_color=clr_lavender_dark,
        bar_color=clr_white,
        direction=VerticalFillDirection.BOTTOM_TO_TOP,
    )
)
_vol_bars.append(
    VerticalProgressBar(
        (vol_bars_width * 3, 0),
        (20, 120),
        fill_color=clr_lavender_dark,
        bar_color=clr_white,
        direction=VerticalFillDirection.BOTTOM_TO_TOP,
    )
)
ui_volume_ind.append(_vol_bars[0])
ui_volume_ind.append(_vol_bars[1])
ui_volume_ind.append(_vol_bars[2])
ui_volume_ind.append(_vol_bars[3])

_vol_bars[0].value = 100
_vol_bars[1].value = 50
_vol_bars[2].value = 25
_vol_bars[3].value = 0

# -----------------------------------
# Render ui_layer_ind
task_label("Rendering layer HUD . . .")


ui_layer_ind.append(
    label.Label(terminalio.FONT, scale=2, x=240, y=40, text="Layer: Null")
)
ui_layer_ind[0].anchor_point = (1.0, 1.0)
ui_layer_ind[0].anchored_position = (320, 120)

# -----------------------------------
# Render ui_layer_popup
task_label("Rendering layer selection popup . . .")

# -----------------------------------
# Render ui_volume_popup
task_label("Rendering volume popup . . .")


ui_volume_popup.append(
    Rect(0, 0, 320, 60, fill=clr_lavender, outline=clr_white, stroke=1)
)
ui_volume_popup.append(
    HorizontalProgressBar(
        (0, 0),
        (320, 30),
        fill_color=clr_lavender_dark,
        bar_color=clr_white,
        direction=HorizontalFillDirection.LEFT_TO_RIGHT,
    )
)
ui_volume_popup.append(
    label.Label(terminalio.FONT, scale=2, x=240, y=40, text="Channel: Null")
)
ui_volume_popup[2].anchor_point = (0.0, 0.0)
ui_volume_popup[2].anchored_position = (5, 30)

ui_volume_popup.append(label.Label(terminalio.FONT, scale=2, x=240, y=40, text="75%"))
ui_volume_popup[3].anchor_point = (1.0, 0.0)
ui_volume_popup[3].anchored_position = (315, 30)

ui_volume_popup[1].value = 75

# -----------------------------------
# Create sleep function

task_label("Creating sleep function . . .")

sleep_display = displayio.Group()
sleep_display.append(
    Rect(0, 0, 320, 240, fill=clr_white)
)

# sleep_timer = 0
# TIME_TO_DIM = 10 # In whole seconds
# TIME_TO_SLEEP = 20 # In whole seconds
# DIM_BRIGHTNESS = 0.01 # Float from 0 to 1

def sleep_routine():
    print("Time since last input: " + str(supervisor.ticks_ms() - (sleep_timer)))

    if supervisor.ticks_ms() - sleep_timer >= (TIME_TO_DIM):
        if display.brightness != DIM_BRIGHTNESS:
            display.brightness = DIM_BRIGHTNESS
    if supervisor.ticks_ms() - sleep_timer >= (TIME_TO_SLEEP):
        if display.brightness != 0 and display.root_group != sleep_display:
            display.brightness = 0
            display.show(sleep_display)
    else:
        if display.brightness != 1 and display.root_group != ui:
            display.show(ui)
            display.brightness = 1

# -----------------------------------
# End boot routine

task_label("Done! <3 Took {} ms".format(str(supervisor.ticks_ms() - timer)))
# Startup tone goes here
time.sleep(2)

# Change display group and clean up boot splash
display.show(ui)

del boot_splash
gc.collect()
print("garbage collected, {} bytes free".format(str(gc.mem_free())))

# -----------------------------------
# Post boot activities

# sleep_timer = supervisor.ticks_ms()

# ui_volume_popup.hidden = True
ui_volume_popup.y = -60

while True:
    # sleep_routine()

    key_event = keys.events.get()
    if key_event:
        print(key_event)
        if key_event.pressed:
            # sleep_timer = supervisor.ticks_ms()
            pixels[key_to_pixel_map(key_event.key_number)] = (170, 62, 224)
        if key_event.released:
            pixels[key_to_pixel_map(key_event.key_number)] = (0, 0, 0)
        # else:
        #     pixels.fill((0, 0, 0))
    # print("(" + str(supervisor.ticks_ms() - timer) + ",)") # Loop speed monitor
    # timer = supervisor.ticks_ms() # Loop speed monitor
    pass
