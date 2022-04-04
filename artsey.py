import board
import time
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

pins = [board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9]

class ReleaseAll:
    pass

layer0 = {
    0x80: [Keycode.A, ReleaseAll()],
    0x09: [Keycode.B, ReleaseAll()],
    0x0c: [Keycode.C, ReleaseAll()],
    0xe0: [Keycode.D, ReleaseAll()],
    0x08: [Keycode.E, ReleaseAll()],
    0xC0: [Keycode.F, ReleaseAll()],
    0x60: [Keycode.G, ReleaseAll()],
    0x0a: [Keycode.H, ReleaseAll()],
    0x02: [Keycode.I, ReleaseAll()],
    0x30: [Keycode.J, ReleaseAll()],
    0x05: [Keycode.K, ReleaseAll()],
    0x0e: [Keycode.L, ReleaseAll()],
    0x07: [Keycode.M, ReleaseAll()],
    0x03: [Keycode.N, ReleaseAll()],
    0x01: [Keycode.O, ReleaseAll()],
    0x0b: [Keycode.P, ReleaseAll()],
    0xb0: [Keycode.Q, ReleaseAll()],
    0x40: [Keycode.R, ReleaseAll()],
    0x10: [Keycode.S, ReleaseAll()],
    0x20: [Keycode.T, ReleaseAll()],
    0x06: [Keycode.U, ReleaseAll()],
    0x50: [Keycode.V, ReleaseAll()],
    0x90: [Keycode.W, ReleaseAll()],
    0x70: [Keycode.X, ReleaseAll()],
    0x04: [Keycode.Y, ReleaseAll()],
    0xf0: [Keycode.Z, ReleaseAll()],
    
    0x88: [Keycode.ENTER, ReleaseAll()],
    0xC1: [Keycode.ESCAPE, ReleaseAll()],
    0x86: [Keycode.GRAVE_ACCENT, ReleaseAll()],
    0xe1: [Keycode.TAB, ReleaseAll()],
    0x84: [Keycode.PERIOD, ReleaseAll()],
    0x18: [Keycode.CONTROL],
    0x82: [Keycode.COMMA, ReleaseAll()],
    0x14: [Keycode.GUI, ReleaseAll()],
    0x81: [Keycode.FORWARD_SLASH, ReleaseAll()],
    0x12: [Keycode.ALT],
    0x22: [Keycode.SHIFT, Keycode.ONE, ReleaseAll()],
    0x78: [Keycode.SHIFT],
    0x0f: [Keycode.SPACE, ReleaseAll()],
    # 0x44 shift lock : don't need
    0x48: [Keycode.BACKSPACE, ReleaseAll()],
    0x87: [Keycode.CAPS_LOCK, ReleaseAll()],
    0x42: [Keycode.DELETE, ReleaseAll()],
    # 0x66 clear bluetooth : don't need
    
    
}

def get_artsey_code(buttons):
    values = [0 if button.value else 1 for button in buttons]
    code = 0
    for value in values:
        code = code * 2 + value
    return code

def artsey():
    buttons = [DigitalInOut(pin) for pin in pins]
    for button in buttons:
        button.direction = Direction.INPUT
        button.pull = Pull.UP

    keyboard = Keyboard(usb_hid.devices)

    artsey_code = 0
    while True:
        code = get_artsey_code(buttons)
        if code < artsey_code:
            #print(artsey_code)
            try:
                print(layer0[artsey_code])
                for e in layer0[artsey_code]:
                    if type(e) is ReleaseAll:
                        keyboard.release_all()
                    else:
                        keyboard.press(e)
            except KeyError:
                pass
            artsey_code = 0
            while code > 0:
                code = get_artsey_code(buttons)
        else:
            artsey_code = code
        time.sleep(0.1)
