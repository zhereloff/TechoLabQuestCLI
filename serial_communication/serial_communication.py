import serial
import time
import re
from colorama import init, Fore, Style

class SerialCommunication:
    def __init__(self):
        self.ser = None
        init(autoreset=True)

    def list_ports(self):
        import serial.tools.list_ports
        ports = serial.tools.list_ports.comports()
        for port in ports:
            print(f"{port.device}: {port.description}")

    def open_port(self, port, baudrate):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            print(f"Connected to {port} at {baudrate} baudrate.")
        except serial.SerialException as e:
            print(f"Error: {e}")

    def close_port(self):
        if self.ser:
            self.ser.close()

    def send_data(self, command):
        if self.ser:
            self.ser.write(command.encode())
            #print(f"Sent: {command}")

    def receive_data(self, data_queue, button_state, log_file=None):
        while True:
            if self.ser and self.ser.is_open:
                data = self.ser.readline().decode().strip()
                if data:
                    if any(pattern in data for pattern in button_state):
                        if "Button pressed" in data:
                            print(Fore.GREEN + "Button pressed")
                        elif "Button held for 5 seconds" in data:
                            print(Fore.YELLOW + "Button held for 5 seconds")
                        elif "Button released" in data:
                            print(Fore.MAGENTA + "Button released")
                        data_queue.put(data)
                    else:
                        adc_match = re.search(r'ADC: (\d+)', data)
                        temp_match = re.search(r'Temperature (\d+) C', data)
                        hum_match = re.search(r'Humidity (\d+)%', data)

                        if adc_match or (temp_match and hum_match):
                            if log_file:
                                self.log_telemetry(log_file, data)
                            data_queue.put(data)

    def log_telemetry(self, log_file, data):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open(log_file, 'a') as f:
            f.write(f"{timestamp} - {data}\n")