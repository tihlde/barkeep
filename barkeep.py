import requests
from led_controller import LedController


def read_password():
    pw = ''
    with open('/home/barkeep/passord', 'r') as file:
        pw = file.read().rstrip('\n\r')
    return pw


class Barkeep:
    rfid_reader = None
    barcode_reader = None
    led_controller = None

    def __init__(self, rfid_reader, barcode_reader, red_pin, green_pin):
        self.rfid_reader = rfid_reader
        self.barcode_reader = barcode_reader
        self.led_controller = LedController(red_pin, green_pin)

    def update(self):
        pass

    def send_request(self, barcode_code):
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
