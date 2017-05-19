# coding: utf-8
import signal
import sys

from barkeep import Barkeep

__author__ = 'Harald Floor Wilhelmsen'

bk = None


def signal_handler(signal, frame):
    global bk
    print("Caught Ctrl+C, shutting down...")
    bk.stop()
    sys.exit()


def main():
    global bk
    rfid_reader_path = '/dev/input/by-id/' \
                       'usb-Sycreader_RFID_Technology_Co.__Ltd_SYC_ID_IC_USB_Reader_08FF20140315-event-kbd'
    signal.signal(signal.SIGINT, signal_handler)
    bk = Barkeep(rfid_reader_path, 0, 1)
    bk.start()


main()
