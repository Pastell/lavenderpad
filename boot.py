# BIOS
'''
Uncomment all lines marked LIVE when the firmware is done and modifications shouldn't be necessary.
The volume control process will be unable to write volume information to disk if the disk can be written to from the computer.

See: https://learn.adafruit.com/circuitpython-essentials/circuitpython-storage
'''

import board
import digitalio
import storage
import supervisor
import usb_midi

# Disable unnecessary USB endpoints. This is for cleanliness, AFAIK the RP2040 has plenty to leave it all enabled
usb_midi.disable()

# Name the drive LavenderPad. The drive name can only be 11 characters, so it just perfectly fits.
# Since any user would be putting the device into edit mode almost immediately, maybe move this in there so it doesn't take up more time on the average boot?
storage.remount("/", readonly=False)
m = storage.getmount("/")
m.label = "LavenderPad"
storage.remount("/", readonly=True)

# Detect interrupt keys. We'll need matrix scan for this, or maybe to save on time, make it a rotary encoder click?
# I'm a clown, we can just do a manual single button scan
col3 = digitalio.DigitalInOut(board.A1)
col3.direction = digitalio.Direction.OUTPUT
col3.value = True
row0 = digitalio.DigitalInOut(board.D10)
row0.direction = digitalio.Direction.INPUT
row0.pull = digitalio.Pull.DOWN

if row0.value == True: # Edit mode interrupt key detected
    print("Booting to edit mode")

    # storage.enable_usb_drive() # LIVE
    # storage.remount("/", True) # LIVE
    supervisor.set_next_code_file("/edit.py")
    supervisor.disable_autoreload()

else: # Proceed as normal
    print("Booting to LavenderPad")

    # storage.disable_usb_drive() # LIVE
    # storage.remount("/", readonly=False) # LIVE
    # supervisor.disable_autoreload() # LIVE

col3.deinit()
row0.deinit()
supervisor.reload()
