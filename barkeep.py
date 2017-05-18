import threading

import requests

import InputReader
from led_controller import LedController


def read_password():
    pw = ''
    with open('/home/barkeep/passord', 'r') as file:
        pw = file.read().rstrip('\n\r')
    return pw


class Barkeep:
    rfid_reader = None
    led_controller = None

    _keep_alive = True
    _t = None

    def __init__(self, rfid_reader_path, red_pin, green_pin):
        self.led_controller = LedController(red_pin, green_pin)
        self.rfid_reader = InputReader.InputReader(
            code_valid_time=15,
            code_validation_pattern='^\d{10}$',
            device_path=rfid_reader_path)

    def _run(self):
        while self._keep_alive:
            self._single_action()

    def _single_action(self):
        if self.rfid_reader.code_is_valid():
            print(self.rfid_reader.get_and_invalidate_code())

    def start(self):
        self._t = threading.Thread(target=self._run)
        self._t.start()
        self._rfid_t = threading.Thread(target=self.rfid_reader.start_read_loop)

    def stop(self):
        self._keep_alive = False
        self._t.join()
        self.rfid_reader.stop()
        self._rfid_t.join()

    def send_request(self):
        response = requests.post('https://driftbar.tihlde.org/buyfromid?', auth=('barkeep', read_password()))
        http_status = response.status_code
        print('Status: ' + str(http_status) + ', text: ' + response.text)
        if not http_status == requests.codes.ok:
            # / error-cause: reaction /
            #  no drinks left: red light, 1 short blink
            # self.led_controller.red_blink(1)
            #  no user tied to that ID: red light, 2 short blinks
            # self.led_controller.red_blink(2)
            #  invalid request: red light, 3 short blinks
            # self.led_controller.red_blink(3)
            pass
        else:
            # success show green LED
            pass
