import time

class TelemetryLogger:
    @staticmethod
    def log_telemetry(log_file, data):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open(log_file, 'a') as f:
            f.write(f"{timestamp} - {data}\n")