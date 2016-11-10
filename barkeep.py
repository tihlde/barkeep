# coding: utf-8
import threading

import cardreader

__author__ = 'Harald Floor Wilhelmsen'


def main():
    reader = cardreader.CardReader()
    threading.Thread(target=reader.read_input).start()
    while 1:
        if reader.code_is_valid():
            print(reader.get_and_invalidate_code())


main()
