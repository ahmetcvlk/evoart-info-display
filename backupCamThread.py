import time
from PyQt5.QtCore import QThread, pyqtSignal
import Jetson.GPIO as GPIO

class BackupCamGpioThread(QThread):
    reverse_changed = pyqtSignal(bool)

    def __init__(self, gpio_pin, parent=None):
        super().__init__(parent)
        self.gpio_pin = gpio_pin
        self._running = True

        GPIO.setmode(GPIO.BOARD)  # Pin numaralandırma şekli, BOARD veya BCM olabilir
        GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Input ve pull-down direnci

    def run(self):
        last_state = None
        while self._running:
            state = GPIO.input(self.gpio_pin)  # GPIO pin değeri oku (0 veya 1)
            if state != last_state:
                self.reverse_changed.emit(bool(state))
                last_state = state
            time.sleep(0.1)  # Çok hızlı döngü olmasın, 100ms uygun

    def stop(self):
        self._running = False
        self.wait()
        GPIO.cleanup(self.gpio_pin)  # Pinleri temizle



