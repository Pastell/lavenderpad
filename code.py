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
import os
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
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_base import KeyboardLayoutBase
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import adafruit_aw9523

# color defs
clr_white = 0xFFFFFF  # Absolute White
clr_lavender = 0xB172C6  # Main UI Lavender
clr_lavender_dark = 0x5D4266  # Darker lavender for backgrounds
clr_red = 0xB70C00

sleep_timer = 0
TIME_TO_DIM = 10000  # In whole seconds
TIME_TO_SLEEP = 20000  # In whole seconds
DIM_BRIGHTNESS = 0.01  # Float from 0 to 1

mode = 0

LAYERS_FOLDER = '/layers'

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
consumer_control = ConsumerControl(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

class Layer:
    def __init__(self, appdata):
        self.name = appdata['name']
        self.macros = appdata['macros']

    def switch(self):
        ui_layer_ind[0].text = self.name
        for i in range(12):
            if i < len(self.macros):
                pixels[key_to_pixel_map(i+4)] = self.macros[i][0]
                _labels[i//4][i%4].text = self.macros[i][1]
            else:
                pixels[key_to_pixel_map(i+4)] = 0
                _labels[i//4][i%4].text = ''

        keyboard.release_all()
        consumer_control.release()
        mouse.release_all()

    def restore_led(self, key):
        if key > 3:
            if key-4 < len(self.macros):
                pixels[key_to_pixel_map(key)] = self.macros[key-4][0]
            else:
                pixels[key_to_pixel_map(key)] = 0
        else:
            pixels[key_to_pixel_map(key)] = (0, 0, 0)



def clamp(num, min_value, max_value):
    num = max(min(num, max_value), min_value)
    return num

def collect():
    saved = gc.mem_free()
    gc.collect()
    print("garbage collected, " + str(gc.mem_free()) + " bytes free, " + str(gc.mem_free() - saved) + " saved")

MODE_MAIN = 0
MODE_LAYERSEL = 1
MODE_DIM = 2
MODE_SLEEP = 3

def stateShiftTo(to):
    global mode

    if to == MODE_MAIN:
        display.show(ui)
    if to == MODE_LAYERSEL:
        updateLayerList(layer_selector)
        display.show(ui_layer_popup)

    if to == MODE_DIM:
        pass
    if to == MODE_SLEEP:
        pass
    mode = to

def loadError(message):
    global task_label
    global display
    global ui_volume_popup
    global boot_splash

    task_label("Critical Error! (x_x#): \n" + message)
    time.sleep(2)

    display.show(ui)
    del boot_splash
    collect()
    try:
        ui_volume_popup.y = -60
    except:
        pass

    while True:
        pass

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
color_bitmap = displayio.Bitmap(320, 240, 2)
color_palette = displayio.Palette(2)
color_palette[0] = clr_lavender
color_palette[1] = clr_red

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


# -----------------------------------
# Initialize the rendering structure
# Variables initialized in back-to-front rendering order
collect()
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
ui.append(ui_volume_popup)

# -----------------------------------
# Render ui_background
collect()
task_label("Initializing key interface . . .")

pixels = neopixel.NeoPixel(board.D25, 16, brightness=0.4)
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
collect()
task_label("Rendering background . . .")


ui_background.append(
    displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
)  # Background matte [0]
ui_background.append(
    Rect(0, 0, 320, 240, fill=clr_lavender, outline=clr_white, stroke=1)
)  # 1px white border [1]

# -----------------------------------
# Render ui_macro_grid
collect()
task_label("Rendering macro grid . . .")


layout = GridLayout(
    x=0,
    y=120,
    width=320,
    height=120,
    grid_size=(4, 3),
    cell_padding=4,
    divider_lines=True,  # divider lines around every cell
    cell_anchor_point=(0.5,0.5)
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
collect()
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
collect()
task_label("Rendering layer HUD . . .")


ui_layer_ind.append(
    label.Label(terminalio.FONT, scale=2, x=240, y=40, text="Layer: Null")
)
ui_layer_ind[0].anchor_point = (1.0, 1.0)
ui_layer_ind[0].anchored_position = (320, 120)

# -----------------------------------
# Render ui_layer_popup
collect()
task_label("Rendering layer selection popup . . .")


ui_layer_popup.append(
    displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
)  # Background matte [0]
ui_layer_popup.append(
    Rect(0, 0, 320, 240, fill=clr_lavender, outline=clr_white, stroke=1)
)  # 1px white border [1]
ui_layer_popup.append(
    Rect(1, 113, 318, 22, fill=clr_lavender_dark, outline=clr_lavender_dark, stroke=1)
)  # selector bar [2]

ui_layer_popup_labels = displayio.Group()
ui_layer_popup.append(ui_layer_popup_labels)  # label group [3]

ui_layer_popup_labels.append(
    label.Label(terminalio.FONT, scale=2, x=240, y=40, text="Layer 1", color=0xC28ED2)
)
ui_layer_popup_labels[0].anchor_point = (0.5, 0.5)
ui_layer_popup_labels[0].anchored_position = (160, 20)

ui_layer_popup_labels.append(
    label.Label(terminalio.FONT, scale=2, x=240, y=40, text="Layer 2", color=0xD2AADD)
)
ui_layer_popup_labels[1].anchor_point = (0.5, 0.5)
ui_layer_popup_labels[1].anchored_position = (160, 45)

ui_layer_popup_labels.append(
    label.Label(terminalio.FONT, scale=2, x=240, y=50, text="Layer 3", color=0xE1C6E8)
)
ui_layer_popup_labels[2].anchor_point = (0.5, 0.5)
ui_layer_popup_labels[2].anchored_position = (160, 70)

ui_layer_popup_labels.append(
    label.Label(terminalio.FONT, scale=2, x=240, y=60, text="Layer 4", color=0xF0E2F4)
)
ui_layer_popup_labels[3].anchor_point = (0.5, 0.5)
ui_layer_popup_labels[3].anchored_position = (160, 95)

ui_layer_popup_labels.append(
    label.Label(terminalio.FONT, scale=2, x=240, y=70, text="Layer 5", color=clr_white)
)
ui_layer_popup_labels[4].anchor_point = (0.5, 0.5)
ui_layer_popup_labels[4].anchored_position = (160, 120)

ui_layer_popup_labels.append(
    label.Label(terminalio.FONT, scale=2, x=240, y=80, text="Layer 6", color=0xF0E2F4)
)
ui_layer_popup_labels[5].anchor_point = (0.5, 0.5)
ui_layer_popup_labels[5].anchored_position = (160, 145)

ui_layer_popup_labels.append(
    label.Label(terminalio.FONT, scale=2, x=240, y=80, text="Layer 7", color=0xE1C6E8)
)
ui_layer_popup_labels[6].anchor_point = (0.5, 0.5)
ui_layer_popup_labels[6].anchored_position = (160, 170)

ui_layer_popup_labels.append(
    label.Label(terminalio.FONT, scale=2, x=240, y=80, text="Layer 8", color=0xD2AADD)
)
ui_layer_popup_labels[7].anchor_point = (0.5, 0.5)
ui_layer_popup_labels[7].anchored_position = (160, 195)

ui_layer_popup_labels.append(
    label.Label(terminalio.FONT, scale=2, x=240, y=80, text="Layer 9", color=0xC28ED2)
)
ui_layer_popup_labels[8].anchor_point = (0.5, 0.5)
ui_layer_popup_labels[8].anchored_position = (160, 220)

def updateLayerList(selector):
    global ui_layer_popup_labels
    i = -4
    for x in range(len(ui_layer_popup_labels)):
        if((layer_selector + i) in range(len(layers))):
            ui_layer_popup_labels[x].text = layers[layer_selector + i].name
        else:
            ui_layer_popup_labels[x].text = ""
        i += 1
# -----------------------------------
# Render ui_volume_popup
collect()
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
collect()
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
# Load layers
collect()
task_label("Loading layers . . .")

layers = []
files = os.listdir(LAYERS_FOLDER)
files.sort()
for filename in files:
    if filename.endswith('.py'):
        try:
            module = __import__(LAYERS_FOLDER + '/' + filename[:-3])
            layers.append(Layer(module.layer))
        except (SyntaxError, ImportError, AttributeError, KeyError, NameError, IndexError, TypeError) as err:
            print("ERROR in", filename)
            import traceback
            traceback.print_exception(err, err, err.__traceback__)

if not layers:
    ui_layer_ind[0].text = "NO LAYERS FOUND"
    print("ERR: NO LAYERS FOUND\nNo layers present in @/layers/, add layer files by entering Edit Mode. Reset the device and hold the Mod key.")
    _labels[0][0].text = "Add la"
    _labels[0][1].text = "yers b"
    _labels[0][2].text = "y ente"
    _labels[0][3].text = "ring  "
    _labels[1][0].text = "Edit M"
    _labels[1][1].text = "ode. H"
    _labels[1][2].text = "old Mo"
    _labels[1][3].text = "d key "
    _labels[2][0].text = "while "
    _labels[2][1].text = "the de"
    _labels[2][2].text = "vice b"
    _labels[2][3].text = "oots. "

    loadError("NO LAYERS FOUND")

# -----------------------------------
# Populate macro grid
collect()
task_label("Populating grid . . .")

layer_index = 0
layer_selector = 0
layers[layer_index].switch()


# -----------------------------------
# Intialize expansion board, rotary encoders
collect()
task_label("Initializing expansion board . . .")

i2c = board.I2C()
aw = adafruit_aw9523.AW9523(i2c)

class RotaryEncoder:
    def __init__(self, pin_a, pin_b, start_val):
        pin_a.direction = digitalio.Direction.INPUT
        pin_b.direction = digitalio.Direction.INPUT

        self.pin_a = pin_a
        self.pin_b = pin_b

        print("pin a")
        print(str(pin_a.value))
        print("pin b")
        print(str(pin_b.value))

        self.val = start_val
        self.previous_state = self.pin_a.value
    def read(self):
        self.current_state = self.pin_a.value

        if self.current_state != self.previous_state:  # True when pulse has occured
            if self.pin_b.value != self.current_state:
                self.val -= 1
                print("Left" + str(self.val))
            else:
                self.val += 1
                print("Right" + str(self.val))
        self.previous_state = self.current_state

vol_channels      = [50, 50, 50, 50]
vol_channels_mute = [0, 0, 0, 0]


# r0_b = aw.get_pin(4)
# r0_a = aw.get_pin(5)
# r1_b = aw.get_pin(6)
# r1_a = aw.get_pin(7)
# r2_b = aw.get_pin(12)
# r2_a = aw.get_pin(13)
# r3_b = aw.get_pin(14)
# r3_a = aw.get_pin(15)

# print(str(r0_b))

encoders = [RotaryEncoder(aw.get_pin(4),aw.get_pin(5),50),
            RotaryEncoder(aw.get_pin(6),aw.get_pin(7),50),
            RotaryEncoder(aw.get_pin(12),aw.get_pin(13),50),
            RotaryEncoder(aw.get_pin(14),aw.get_pin(15),50)]
#
# encoders_last_pos = [encoders[0].position,
#                      encoders[1].position,
#                      encoders[2].position,
#                      encoders[3].position]

# -----------------------------------
# End boot routine

task_label("Done! <3 Took {} ms".format(str(supervisor.ticks_ms() - timer)))
# Startup tone goes here
time.sleep(2)

# Change display group and clean up boot splash
display.show(ui)

del boot_splash
collect()

# -----------------------------------
# Post boot activities

# sleep_timer = supervisor.ticks_ms()

# ui_volume_popup.hidden = True
ui_volume_popup.y = -60
encoders_range = range(len(encoders))
while True:
    if mode == MODE_MAIN:  # Normal UI

        # Encoders
        for i in encoders_range:
            encoders[i].read()

        # Keys
        key_event = keys.events.get()
        if key_event:
            print("mode: " + str(mode) + ", key event: " + str(key_event))

            if key_event.pressed:
                if key_event.key_number <= 3:
                    if key_event.key_number == 0:  # Back
                        consumer_control.release()
                        consumer_control.press(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
                        consumer_control.release()
                    if key_event.key_number == 1:  # Play/Pause
                        consumer_control.release()
                        consumer_control.press(ConsumerControlCode.PLAY_PAUSE)
                        consumer_control.release()
                    if key_event.key_number == 2:  # Forward
                        consumer_control.release()
                        consumer_control.press(ConsumerControlCode.SCAN_PREVIOUS_TRACK)
                        consumer_control.release()
                    if key_event.key_number == 3:  # Modifier
                        stateShiftTo(MODE_LAYERSEL)

                pixels[key_to_pixel_map(key_event.key_number)] = (170, 62, 224)
                if key_event.key_number - 4 >= len(layers[layer_index].macros):
                    continue

                if key_event.key_number >= 4:
                    sequence = layers[layer_index].macros[key_event.key_number - 4][2]
                    for item in sequence:
                        if isinstance(item, int):
                            if item >= 0:
                                keyboard.press(item)
                            else:
                                keyboard.release(-item)
                        elif isinstance(item, float):
                            time.sleep(item)
                        elif isinstance(item, str):
                            keyboard_layout.write(item)
                        elif isinstance(item, list):
                            for code in item:
                                if isinstance(code, int):
                                    consumer_control.release()
                                    consumer_control.press(code)
                                if isinstance(code, float):
                                    time.sleep(code)
                        elif isinstance(item, dict):
                            if 'buttons' in item:
                                if item['buttons'] >= 0:
                                    mouse.press(item['buttons'])
                                else:
                                    mouse.release(-item['buttons'])
                            mouse.move(item['x'] if 'x' in item else 0,
                                       item['y'] if 'y' in item else 0,
                                       item['wheel'] if 'wheel' in item else 0)
            if key_event.released:
                if key_event.key_number >= 4:
                    for item in sequence:
                        if isinstance(item, int):
                            if item >- 0:
                                keyboard.release(item)
                        elif isinstance(item, dict):
                            if 'buttons' in item:
                                if item['buttons'] >= 0:
                                    mouse.release(item['buttons'])
                    consumer_control.release()

                layers[layer_index].restore_led(key_event.key_number)

    if mode == MODE_LAYERSEL:
        key_event = keys.events.get()
        if key_event:
            print("mode: " + str(mode) + ", key event: " + str(key_event))

            if key_event.pressed:
                if key_event.key_number <= 3:
                    if key_event.key_number == 0:  # Layer Back
                        layer_selector = clamp((layer_selector - 1), 0, (len(layers)-1))
                        print("layer selector: " + str(layer_selector))
                        updateLayerList(layer_selector)
                    if key_event.key_number == 1:  # Null
                        pass
                    if key_event.key_number == 2:  # Layer Forward
                        layer_selector = clamp((layer_selector + 1), 0, (len(layers)-1))
                        print("layer selector: " + str(layer_selector))
                        updateLayerList(layer_selector)
                    if key_event.key_number == 3:  # Modifier
                        pass
                pixels[key_to_pixel_map(key_event.key_number)] = (170, 62, 224)

            if key_event.released:
                if key_event.key_number <= 3:
                    if key_event.key_number == 3:
                        layer_index = layer_selector
                        layers[layer_index].switch()
                        stateShiftTo(MODE_MAIN)
                layers[layer_index].restore_led(key_event.key_number)
    pass
