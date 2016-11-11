# coding: utf-8
import threading

import cardreader
import InputReader

__author__ = 'Harald Floor Wilhelmsen'


def main():
    rfid_card_reader = \
        InputReader.InputReader(
            code_valid_time=15,
            code_validation_pattern='^\d{10}$',
            device_path=
            '/dev/input/by-id/usb-Sycreader_RFID_Technology_Co.__Ltd_SYC_ID_IC_USB_Reader_08FF20140315-event-kbd')
    threading.Thread(target=rfid_card_reader.start_read_loop).start()

    # reader = cardreader.CardReader()
    # threading.Thread(target=reader.read_input).start()
    # while 1:
    #     if reader.code_is_valid():
    #         print(reader.get_and_invalidate_code())


main()
