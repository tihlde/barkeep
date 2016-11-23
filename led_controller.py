from gpiozero import LED


class LedController:
    red = None
    green = None

    on_and_off_time = 0.1

    def __init__(self, red_led_pin, green_led_pin):
        self.red = LED(red_led_pin)
        self.green = LED(green_led_pin)

    def red_blink(self, amount):
        self.red.blink(self.on_and_off_time, self.on_and_off_time, amount)

    def green_blink(self, amount):
        self.green.blink(self.on_and_off_time, self.on_and_off_time, amount)
