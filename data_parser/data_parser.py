import re

class DataParser:
    @staticmethod
    def parse_data(data):
        adc_match = re.search(r'ADC: (\d+)', data)
        temp_match = re.search(r'Temperature (\d+) C', data)
        hum_match = re.search(r'Humidity (\d+)%', data)

        adc_value = int(adc_match.group(1)) if adc_match else None
        temperature = int(temp_match.group(1)) if temp_match else None
        humidity = int(hum_match.group(1)) if hum_match else None
        
        return adc_value, temperature, humidity