# coding: utf-8
import re
import time

import evdev
from evdev import InputDevice

__author__ = 'Harald Floor Wilhelmsen'


class CardReader:
    SCAN_CODES = {
        # Scancode: ASCIICode
        0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
        10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
        20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
        30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
        40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
        50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
    }

    CODE_VALID_PATTERN = '^\d{10}$'
    CODE_VALID_TIME = 15

    card_code = ''
    time_read = 0
    dev = InputDevice('/dev/input/by-id/usb-Sycreader_RFID_Technology_Co.__Ltd_SYC_ID_IC_USB_Reader_08FF20140315-event-kbd')

    def get_age(self):
        # returns age in seconds
        return time.time() - self.time_read

    def code_is_valid(self):
        return re.match(self.CODE_VALID_PATTERN, self.card_code) and self.get_age() <= self.CODE_VALID_TIME

    def get_and_invalidate_code(self):
        self.time_read = 0
        return self.card_code

    def read_input(self):
        read_so_far = ''
        for event in self.dev.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                data = evdev.categorize(event)  # Save the event temporarily to introspect it
                if data.keystate == 1:  # Down events only
                    if data.scancode == 28:
                        self.card_code = read_so_far
                        read_so_far = ''
                        self.time_read = time.time()
                    else:
                        key_lookup = self.SCAN_CODES.get(data.scancode)
                        read_so_far += key_lookup
