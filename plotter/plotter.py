import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
import datetime
from matplotlib.widgets import Button
from data_parser.data_parser import DataParser

class Plotter:
    def __init__(self, log_file, plotter_points = 100):
        self.log_file = log_file
        self.plotter_points = plotter_points
        self.ani = None

    def show_plot(self):
        fig, (ax1, ax2) = plt.subplots(2, 1)
        xs_adc, xs_temp_hum, adc_ys, temp_ys, hum_ys = [], [], [], [], []

        def update(frame):
            try:
                with open(self.log_file, 'r') as f:
                    lines = f.readlines()

                temp_xs_adc, temp_xs_temp_hum, temp_adc_ys, temp_temp_ys, temp_hum_ys = [], [], [], [], []

                for line in lines[-self.plotter_points:]: 
                    if ' - ' in line:
                        timestamp_str, data = line.split(' - ', 1)
                        timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                        adc_value, temperature, humidity = DataParser.parse_data(data)
                        
                        if adc_value is not None:
                            temp_xs_adc.append(timestamp)
                            temp_adc_ys.append(adc_value)
                        if temperature is not None and humidity is not None:
                            temp_xs_temp_hum.append(timestamp)
                            temp_temp_ys.append(temperature)
                            temp_hum_ys.append(humidity)

                if temp_xs_adc:
                    xs_adc.clear()
                    adc_ys.clear()
                    xs_adc.extend(temp_xs_adc)
                    adc_ys.extend(temp_adc_ys)
                if temp_xs_temp_hum:
                    xs_temp_hum.clear()
                    temp_ys.clear()
                    hum_ys.clear()
                    xs_temp_hum.extend(temp_xs_temp_hum)
                    temp_ys.extend(temp_temp_ys)
                    hum_ys.extend(temp_hum_ys)

                ax1.clear()
                ax2.clear()
                ax1.plot(xs_adc, adc_ys, label='ADC Value')
                ax2.plot(xs_temp_hum, temp_ys, label='Temperature', color='r')
                ax2.plot(xs_temp_hum, hum_ys, label='Humidity', color='b')

                ax1.set_title('ADC Value Over Time')
                ax2.set_title('Temperature and Humidity Over Time')
                ax1.set_xlabel('Time')
                ax1.set_ylabel('ADC Value')
                ax2.set_xlabel('Time')
                ax2.set_ylabel('Value')
                ax1.legend()
                ax2.legend()

                ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
                ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

                ax1.tick_params(axis='x', labelsize=8)
                ax2.tick_params(axis='x', labelsize=8)

                fig.autofmt_xdate()
            except Exception as e:
                print(f"Error updating plot: {e}")

        def stop(event):
            if self.ani:
                self.ani.event_source.stop()

        def start(event):
            if self.ani:
                self.ani.event_source.start()

        axstart = plt.axes([0.7, 0.01, 0.1, 0.075])
        axstop = plt.axes([0.81, 0.01, 0.1, 0.075])
        bstart = Button(axstart, 'Start')
        bstop = Button(axstop, 'Stop')
        bstart.on_clicked(start)
        bstop.on_clicked(stop)

        self.ani = animation.FuncAnimation(fig, update, interval=1000)
        plt.show()
