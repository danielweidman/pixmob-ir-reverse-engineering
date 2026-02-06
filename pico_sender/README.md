This folder contains the code for a [Raspberry Pi Pico](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html) that will listen for commands over serial from a computer and then transmit those IR commands with an attached IR transmitter.

You need to have a simple IR transmitter circuit set up with your Pico. This can be accomplished with a board like [this](https://www.amazon.com/Digital-Receiver-Transmitter-Arduino-Compatible/dp/B01E20VQD8/) or an IR LED with a resistor and/or transistor. Many tutorials are available for the simple circuit.

The Pico code is written in MicroPython, which means that you need to have MicroPython set up to execute it. You can either [drag and drop](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html#drag-and-drop-micropython) MicroPython onto your Pico or install it [using Thonny](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/3). 

Once you write the [main.py file](PixMob_Transmitter_Pico/main.py) to your Pico, it is ready to receive commands over serial. The main.py file gets executed automatically once you plug your Pico in.
