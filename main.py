import argparse
import threading
import queue
from serial_communication.serial_communication import SerialCommunication
from plotter.plotter import Plotter
from RGB_control.RGB_control import RGBcontrol
from CLI_menu.CLI_menu import CLIMenu

LOG_FILE = "telemetry.log"
DATA_QUEUE = queue.Queue()
BUTTON_STATE = ["Button pressed", "Button held for 5 seconds", "Button released"]

def main():
    global LOG_FILE

    parser = argparse.ArgumentParser(description="UART communication script.")
    parser.add_argument("--list", action="store_true", help="List all available serial ports")
    parser.add_argument("--port", type=str, help="Serial port to connect to")
    parser.add_argument("--baudrate", type=int, default=9600, help="Baudrate for the serial connection")
    parser.add_argument("--log", type=str, default=LOG_FILE, help="File to log received data")

    args = parser.parse_args()

    serial_comm = SerialCommunication()
    if args.list:
        serial_comm.list_ports()
        return

    if not args.port:
        print("Please specify a serial port with --port ")
        return

    LOG_FILE = args.log

    serial_comm.open_port(args.port, args.baudrate)
    if serial_comm.ser:
        receive_thread = threading.Thread(target=serial_comm.receive_data, args=(DATA_QUEUE, BUTTON_STATE, LOG_FILE))
        receive_thread.daemon = True
        receive_thread.start()

        plotter = Plotter(LOG_FILE)
        slider_window = RGBcontrol(serial_comm)
        menu = CLIMenu(serial_comm, plotter, slider_window)
        menu.show_menu()

        serial_comm.close_port()
        receive_thread.join()

if __name__ == "__main__":
    main()
