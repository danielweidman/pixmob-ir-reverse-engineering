This folder contains the code for an Arduino that will listen for commands over serial from a computer and then transmit those IR commands with an attached IR transmitter.

You need to have a simple IR transmitter circuit set up with your Arduino. This can be accomplished with a board like [this](https://www.amazon.com/Digital-Receiver-Transmitter-Arduino-Compatible/dp/B01E20VQD8/) or an IR LED with a resistor and/or transistor. Many tutorials are available for the simple circuit.

There are two Arduino sketches available. One is for an ESP32 specifically, and the other is for other Arduino-compatible devices. The difference is that the ESP32 version can take commands over Bluetooth in addition to USB serial, so it could be controlled wirelessly.