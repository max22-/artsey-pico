import board
import time
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

pins = [board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9]

layer0 = {
    128 : 'a',
    64 : 'r',
    32: 't',
    16: 's',
    8: 'e',
    4: 'y',
    2: 'i',
    1: 'o',
    9: 'b',
    12: 'c',
    224: 'd',
    192: 'f',
    96: 'g',
    10: 'h',
    48: 'j',
    5: 'k',
    14: 'l',
    7: 'm',
    3: 'n',
    11: 'p',
    176: 'q',
    6: 'u',
    80: 'v',
    144: 'w',
    112: 'x',
    240: 'z'
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
                keyboard.press(Keycode.A)
                keyboard.release_all()
            except KeyError:
                pass
            artsey_code = 0
            while code > 0:
                code = get_artsey_code(buttons)
        else:
            artsey_code = code
        time.sleep(0.1)