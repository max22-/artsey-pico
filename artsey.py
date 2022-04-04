import board
import time
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

pins = [board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9]

class State:
    BASE = 0
    NAV = 1
    NUMBERS = 2

class ReleaseAll:
    pass

layer_base = {
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

layer_nav = {
    0x80: [Keycode.HOME, ReleaseAll()],
    0x40: [Keycode.UP_ARROW, ReleaseAll()],
    0x20: [Keycode.END, ReleaseAll()],
    0x10: [Keycode.PAGE_UP, ReleaseAll()],
    0x08: [Keycode.LEFT_ARROW, ReleaseAll()],
    0x04: [Keycode.DOWN_ARROW, ReleaseAll()],
    0x02: [Keycode.RIGHT_ARROW, ReleaseAll()],
    0x01: [Keycode.PAGE_DOWN, ReleaseAll()],
}

layer_numbers = {
    0x16: [Keycode.ZERO, ReleaseAll()],
    0x90: [Keycode.ONE, ReleaseAll()],
    0x50: [Keycode.TWO, ReleaseAll()],
    0x30: [Keycode.THREE, ReleaseAll()],
    0x18: [Keycode.FOUR, ReleaseAll()],
    0x14: [Keycode.FIVE, ReleaseAll()],
    0x12: [Keycode.SIX, ReleaseAll()],
    0xd0: [Keycode.SEVEN, ReleaseAll()],
    0x70: [Keycode.EIGHT, ReleaseAll()],
    0x1c: [Keycode.NINE, ReleaseAll()], 
}

def play_code(code, layer, keyboard):
    if code in layer.keys():
        for e in layer[code]:
            if type(e) is ReleaseAll:
                keyboard.release_all()
            else:
                keyboard.press(e)


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

    state = State.BASE
    code = 0
    timestamp = time.time()
    while True:
        new_code = get_artsey_code(buttons)
        if new_code != code:
            timestamp = time.time()
        new_timestamp = time.time()
        if new_timestamp - timestamp > 0.2:
            if code == 0x10:
                state = State.NUMBERS
                
        if new_code < code:
            if state == State.BASE:
                if code == 0x4a:
                    state = State.NAV
                play_code(code, layer_base, keyboard)
                while new_code > 0:
                    new_code = get_artsey_code(buttons)
                
            elif state == State.NAV:
                if code == 0x4a:
                    state = State.BASE
                play_code(code, layer_nav, keyboard)

            elif state == State.NUMBERS:
                play_code(code, layer_numbers, keyboard)
                while new_code > 0 and new_code != 0x10:
                    new_code = get_artsey_code(buttons)
                if new_code == 0:
                    state = State.BASE
            
        code = new_code
        time.sleep(0.1)
