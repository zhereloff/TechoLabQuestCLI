import threading
from colorama import init, Fore, Style

class CLIMenu:
    def __init__(self, serial_comm, plotter, slider_window):
        self.serial_comm = serial_comm
        self.plotter = plotter
        self.slider_window = slider_window
        init(autoreset=True)

    def show_menu(self):
        while True:
            print(Fore.RED + f"\n{Style.BRIGHT}   MENU:")
            print(f"{Fore.CYAN}1. Ports")
            print(f"{Fore.CYAN}2. Send Data")
            print(f"{Fore.CYAN}3. Plot Data")
            print(f"{Fore.CYAN}4. Exit")
            choice = input(Fore.LIGHTYELLOW_EX + "Enter your choice: ")

            if choice == '1':
                self.serial_comm.list_ports()
            elif choice == '2':
                self.slider_window.open_window() 
            elif choice == '3':
                self.plotter.show_plot()
            elif choice == '4':
                self.serial_comm.close_port()
                break
            else:
                print("Invalid choice. Please try again.")
