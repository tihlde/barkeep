import threading

import requests
from requests.auth import HTTPBasicAuth

import InputReader
from led_controller import LedController


class Barkeep:
    _rfid_reader = None
    _led_controller = None

    _keep_alive = True
    _t = None
    _rfid_t = None
    _password = None

    def __init__(self, rfid_reader_path, red_pin, green_pin):
        self._led_controller = LedController(red_pin, green_pin)
        self._rfid_reader = InputReader.InputReader(
            code_valid_time=15,
            code_validation_pattern='^\d{10}$',
            device_path=rfid_reader_path)
        self._rfid_t = threading.Thread(target=self._rfid_reader.start_read_loop)
        with open('/home/barkeep/passord', 'r') as file:
            self._password = file.read().rstrip('\n\r')
        print('barkeep started with pw', self._password)

    def _run(self):
        while self._keep_alive:
            self._single_action()
        print('Barkeep stopped')

    def _single_action(self):
        if self._rfid_reader.code_is_valid():
            # send request
            code = self._rfid_reader.get_and_invalidate_code()
            print(code)
            success = self._send_request(code, 2)
            if not success:
                # / error-cause: reaction /
                #  no drinks left: red light, 1 short blink
                # self.led_controller.red_blink(1)
                #  no user tied to that ID: red light, 2 short blinks
                # self.led_controller.red_blink(2)
                #  invalid request: red light, 3 short blinks
                # self.led_controller.red_blink(3)
                print('not success')
            else:
                # success show green LED
                print('success')

    def start(self):
        self._t = threading.Thread(target=self._run)
        self._t.start()
        self._rfid_t.start()

    def stop(self):
        self._keep_alive = False
        self._t.join()
        self._rfid_reader.stop()
        self._rfid_t.join()

    def _send_request(self, code, drink_id):
        # /decbarkeep/<ntnu>/<drikkeid>
        response = requests.get('https://driftbar.tihlde.org/decbarkeep/{0}/{1}'.format(code, drink_id),
                                auth=HTTPBasicAuth('barkeep', self._password))
        http_status = response.status_code
        print('Status: ' + str(http_status) + ', text: ' + response.text)
        return http_status == requests.codes.ok
