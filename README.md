# Lavenderpad 
### A DIY programmable macropad & physical volume mixer

*Lavenderpad* is my project to create a fully custom programmable macropad and physical volume mixer.

### 1: Goals
1. Individual macro profiles, called Layers, must be loaded from a human-readable, and more importantly human-writable, file.
2. Layers must be switchable on the fly.
3. Each individual Macro must be capable of outputting a sequence of keystrokes, mouse actions, and consumer control codes.
4. Each key's function in any given layer must be maximally legible to the user.
5. The device must contain a set of rotary encoders (knobs) that can change the volume of or mute a certain selection of applications on a host computer.
6. The volume of any given channel at any given time must be maximally legible to the user.
7. The device must be able to operate for extending periods of time without compromising it's function or physical integrity.
8. The final physical object must resemble a professional produced product, at least on the outside.

### 2: Implementation
As someone who frankly has little to no idea what they are doing, much of this project's code is derived or copied from various other open-source projects.

#### 2.1: Macros
The macro handling is derived almost entirely from Phillip Burgess' [*MACROPAD Hotkeys*](https://learn.adafruit.com/macropad-hotkeys), a macropad implementation designed to work on Adafruit's *MacroPad RP2040* board.

Other inspirations include Ken Baskett's [*App Pad*](https://github.com/kbaskett248/adafruit_macropad), and John Ellis' [*Macropad Hotkeys II*](https://github.com/deckerego/Macropad_Hotkeys), both forks of the original *MACROPAD Hotkeys*.

#### 2.2: Volume Control
Volume control handling on the peripheral side will be my own code, outputting data through USB Serial that is interpreted by a host-side app, Brent Claessens' [fork](https://github.com/YaMoef/deej) of the original [*Deej*](https://github.com/omriharel/deej) host side app. *Deej* is an open-source project for creating a physical potentiometer-based mixer for the Windows digital mixer. Brent Claeseens modified the original host app to accept a 0-100 integer for each channel and directly apply that to the corresponding digital mixer channel, rather than *Deej*'s host-side potentiometer value mapping. This makes it perfect for client-side volume management using a rotary encoder interface.

#### 2.3: Physical Device
The current protype consists of breadboard mounted components. As per Goal 8, I intend to create a 3D-printed case for the device. The design is not finalized, but I am keeping in mind a few design considerations:
1. The frame of the device ought to match that of my *Keychron C2* keyboard, such that if I placed them side to side, the macropad would seem like part of the original keyboard.
2. The screen must be canted toward the user, as the screen may be otherwise obscured by keycaps or knobs, or simply a poor viewing angle (TFTs do not have great viewing angles, at least compared to IPS panels.)
3. The USB-C port of the *Feather RP2040* must be accessible from the back of the device for interfacing.
4. A hard-wired reset button (Pulling the RST pin to GND) must be accessible without taking apart the device.

### 3: Material Cost
The current prototype consists of the following, all sourced from Adafruit:
```
1. Adafruit Feather RP2040                    = $11.95
2. Adafruit 2.2" 18-bit TFT LCD breakout      = $24.95
3. 4x PEC11-4215F-S24 rotary encoders         = $18.00
4. Adafruit NeoKey 5x6 Ortholinear Snap-Apart = $29.95
5. 16x Kalih Red mechanical switches          = $13.90 (four switches left over)
6. Adafruit AW9523 GPIO Expander breakout     = $4.95
-------------------------------------------------------
   Total, without tax or shipping             = $103.7
```
