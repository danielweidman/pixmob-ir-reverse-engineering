import argparse
import logging
import time
from typing import Optional

import serial

from python_tools.effect_definitions import (
    base_color_effects,
    special_effects,
    tail_codes,
)
from python_tools.pixmob_conversion_funcs import bits_to_arduino_string

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
)

LOG = logging.getLogger(__name__)


def print_help():
    print(
        "Command syntax:",
        " BASE_EFFECT [TAIL_CODE]",
        " SPECIAL_EFFECT [TAIL_CODE]",
        "Base effects:",
        " ".join(base_color_effects.keys()),
        "",
        "Special effects:",
        " ".join(special_effects.keys()),
        "",
        "Tail codes:",
        " ".join(tail_codes.keys()),
        "",
        "Example:",
        " %s" % next(iter(base_color_effects.keys())),
        " %s %s"
        % (next(iter(base_color_effects.keys())), next(iter(tail_codes.keys()))),
        sep="\n",
    )


def send_effect(
    serial_port: serial.Serial, effect_code: str, tail_code: Optional[str] = None
):
    effect_bits = []

    effect_code = effect_code.upper().strip()

    if effect_code in base_color_effects:
        effect_bits = base_color_effects[effect_code]
    elif effect_code in special_effects:
        effect_bits = special_effects[effect_code]
    else:
        LOG.warning(
            "Invalid base effect %s. See base_color_effects and "
            "special_effects in effect_definitions.py for options.",
            effect_code,
        )
        return

    # NOTE: Not sure if special effects also take tail code input
    if tail_code is not None:
        tail_code = tail_code.upper().strip()

        if tail_code in tail_codes:
            effect_bits += tail_codes[tail_code]
        else:
            LOG.warning(
                "Invalid tail code %s. See tail_codes "
                "in effect_definitions.py for options.",
                tail_code,
            )

    arduino_string_ver = bits_to_arduino_string(effect_bits)
    tx_data = bytes(arduino_string_ver, "utf-8")
    LOG.debug("Transmitting %s...", tx_data[:32])

    serial_port.write(tx_data)

    # Small delay after each command
    time.sleep(0.1)


def repl_commands(serial_port: serial.Serial):
    print('Type "help" for a list of known commands, "exit" or "q" to quit.')
    while True:
        try:
            cmd = input("Command> ")
        except KeyboardInterrupt:
            break

        # Split by space to add tail command after base command.
        cmd = cmd.upper().split(" ")

        if cmd[0] == "EXIT" or cmd[0] == "Q":
            break

        if cmd[0] == "HELP":
            print_help()
            continue

        effect_code = cmd[0]
        tail_code = cmd[1] if len(cmd) > 1 else None
        send_effect(serial_port, effect_code, tail_code=tail_code)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Simple command-line loop to send effects "
            "to the Pixmob bracelet by typing in the effect names."
        )
    )
    parser.add_argument(
        "-p",
        "--port",
        default="/dev/ttyUSB0",
        type=str,
        help="Serial port (COMx, /dev/ttyUSB0 or /dev/ttyACM0) to connect.",
    )
    parser.add_argument(
        "-b",
        "--baud-rate",
        default=115200,
        type=int,
        help="Serial baud rate (default: 115200)",
    )
    parser.add_argument(
        "-w",
        "--wait-on-connect",
        action="store_true",
        default=False,
        help=(
            "Set to True if using a lower power microcontroller "
            "(like an Arduino Nano instead of ESP board) "
            "and you have issues."
        ),
    )
    parser.add_argument(
        "-c",
        "--continue-cli",
        action="store_true",
        default=False,
        help=(
            "Set to True if you are passing the effect in the "
            "command line, and want to still drop into the REPL."
        ),
    )

    parser.add_argument("effect", type=str, nargs="?")
    parser.add_argument("tail_code", type=str, nargs="?")

    args = parser.parse_args()

    try:
        LOG.info("Connecting to %s at baud rate %d...", args.port, args.baud_rate)
        arduino = serial.Serial(port=args.port, baudrate=args.baud_rate, timeout=0.1)
        LOG.info("Connected!")
    except Exception:
        LOG.exception("Failed while trying to connect. Full traceback:")
        print(
            "If you haven't, specify the serial port to connect to using "
            "the '-p' argument."
        )
        print("Run the script with '-h' for more information.")
        exit(1)

    try:
        if args.wait_on_connect:
            time.sleep(2.5)

        # If user has provided effect in arguments, send it directly
        if args.effect is not None:
            send_effect(arduino, args.effect, tail_code=args.tail_code)
            # If the program should not go to the repl after done, exit.
            if not args.continue_cli:
                return

        repl_commands(arduino)
    except Exception:
        LOG.exception("Uncaught exception occurred in the input loop. Full traceback:")
    finally:
        arduino.close()


if __name__ == "__main__":
    main()
