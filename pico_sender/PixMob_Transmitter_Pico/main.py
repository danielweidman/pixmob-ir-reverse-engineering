from machine import Pin, PWM
from time import sleep_us

import select
import sys

poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

ir_pin = Pin(15, Pin.OUT)  # set this to the data pin used for the IR LED
ir_led = PWM(ir_pin)
ir_led.freq(38000)


def read_until(until_char, keep_result=True):
    result = ''
    while True:
        char = sys.stdin.read(1)
        if char == until_char:
            break

        if keep_result:
            result += char
    return result


def send_raw_ir_command(command, ir_pin):
    for i in range(len(command)):
        duration = int(command[i]) * 700
        if i % 2 == 0:
            ir_pin.duty_u16(32768)  # 50% duty cycle
        else:  # Odd index (space)
            ir_pin.duty_u16(0)
        sleep_us(duration)
    ir_pin.deinit()


while True:
    poll_results = poll_obj.poll(1)
    if poll_results:
        read_until(']', False)
        command = read_until(',')
        send_raw_ir_command(command, ir_led)
