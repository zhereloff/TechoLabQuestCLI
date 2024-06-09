import tkinter as tk
from tkinter import ttk

class RGBcontrol:
    def __init__(self, serial_comm):
        self.serial_comm = serial_comm

    def update_value(self, event, red_slider, green_slider, blue_slider):
        r = int(red_slider.get())
        g = int(green_slider.get())
        b = int(blue_slider.get())
        command = f"{r:03}{g:03}{b:03}"
        self.serial_comm.send_data(command)

    def create_slider(self, parent, label_text, row):
        ttk.Label(parent, text=label_text).grid(column=0, row=row)
        slider = tk.Scale(parent, from_=0, to=255, orient='horizontal')
        slider.grid(column=1, row=row)
        return slider

    def open_window(self):
        slider_window = tk.Tk()
        slider_window.title("Send Data")

        red_slider = self.create_slider(slider_window, "Red", 0)
        green_slider = self.create_slider(slider_window, "Green", 1)
        blue_slider = self.create_slider(slider_window, "Blue", 2)

        red_slider.bind("<Motion>", lambda event: self.update_value(event, red_slider, green_slider, blue_slider))
        green_slider.bind("<Motion>", lambda event: self.update_value(event, red_slider, green_slider, blue_slider))
        blue_slider.bind("<Motion>", lambda event: self.update_value(event, red_slider, green_slider, blue_slider))

        slider_window.mainloop()