# coding: utf-8
import threading

import InputReader

__author__ = 'Harald Floor Wilhelmsen'

using_bar_code_reader = False


def create_barcode_scanner(code_valid_time=15):
    return InputReader.InputReader(
        code_valid_time=code_valid_time,
        code_validation_pattern='^\d{13}$',
        device_path='/dev/input/by-id/'
                    'usb-13ba_Barcode_Reader-event-kbd')


def create_rfid_reader(code_valid_time=15):
    return InputReader.InputReader(
        code_valid_time=code_valid_time,
        code_validation_pattern='^\d{10}$',
        device_path='/dev/input/by-id/'
                    'usb-Sycreader_RFID_Technology_Co.__Ltd_SYC_ID_IC_USB_Reader_08FF20140315-event-kbd')


def main():
    global using_bar_code_reader
    try:
        barcode_reader = create_barcode_scanner()
        threading.Thread(target=barcode_reader.start_read_loop).start()
        using_bar_code_reader = True
    except FileNotFoundError:
        print('No barcode-reader found')

    rfid_card_reader = create_rfid_reader()
    threading.Thread(target=rfid_card_reader.start_read_loop).start()

    while 1:
        if rfid_card_reader.code_is_valid():
            print(rfid_card_reader.get_and_invalidate_code())
        if using_bar_code_reader and barcode_reader.code_is_valid():
            print(barcode_reader.get_and_invalidate_code())


main()
