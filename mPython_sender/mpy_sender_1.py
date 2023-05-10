# import IRremote # Replace this with the appropriate MicroPython library for IR

# SET THIS TO THE DATA PIN USED FOR THE IR TRANSMITTER
kIrLed = 4

incoming_string = ""

def setup():
    global kIrLed
    # Initialize Serial communication
    
    from machine import UART

    uart = UART(0, 230400)
    
    # Initialize IR sender
    # IrSender.begin(kIrLed)
    # IrSender.enableIROut(38)
    pass

def loop():
    global incoming_string
    # Uncomment and replace the following lines with the appropriate MicroPython library for IR
    # while not uart.any():
    #     pass
    
    # incoming_string = uart.readline().decode().split('[')[1] # read the incoming byte
    # incoming_string = incoming_string.split(']')[0] # read the incoming byte

    new_length = int(incoming_string)
    new_raw_data = [0] * new_length
    new_vals = incoming_string.split(',')
    for i in range(len(new_vals)):
        int_val = int(new_vals[i]) * 700
        new_raw_data[i] = int_val
    
    # IrSender.sendRaw(new_raw_data, new_length, 38)  # Send a raw data capture at 38kHz.
    import utime
    utime.sleep_ms(3)

setup()

while True:
    loop()
