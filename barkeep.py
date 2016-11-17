# coding: utf-8
import threading

import InputReader

__author__ = 'Harald Floor Wilhelmsen'


def main():
    barcode_reader = \
        InputReader.InputReader(
            code_valid_time=15,
            code_validation_pattern='^\d{13}$',
            device_path=
            '/dev/input/by-id/usb-13ba_Barcode_Reader-event-kbd')

    threading.Thread(target=barcode_reader.start_read_loop).start()

    rfid_card_reader = \
        InputReader.InputReader(code_valid_time=15,
                                code_validation_pattern='^\d{10}$',
                                device_path='/dev/input/by-id/usb-Sycreader_'
                                            'RFID_Technology_Co.__Ltd_SYC_ID_IC_USB_Reader_08FF20140315-event-kbd')
    threading.Thread(target=rfid_card_reader.start_read_loop).start()

    while 1:
        if rfid_card_reader.code_is_valid():
            print(rfid_card_reader.get_and_invalidate_code())
        if barcode_reader.code_is_valid():
            print(barcode_reader.get_and_invalidate_code())


main()
