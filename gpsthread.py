from PyQt5.QtCore import QThread, pyqtSignal
import serial

class GPSThread(QThread):
    konum_guncelle = pyqtSignal(float, float)

    def run(self):
        ser = serial.Serial("/dev/ttyTHS1", 9600, timeout=1)
        while True:
            try:
                line = ser.readline().decode('ascii', errors='replace').strip()
                loc = self.parse_gga(line)
                if loc:
                    self.konum_guncelle.emit(loc[0], loc[1])
            except Exception as e:
                print("GPS Hata:", e)
                break
    
    def parse_gga(self,sentence):
        try:
            parts = sentence.split(",")
            if parts[0].endswith("GGA") and parts[6] != "0":
                # Enlem
                lat_raw = parts[2]
                lat_dir = parts[3]
                lon_raw = parts[4]
                lon_dir = parts[5]

                lat_deg = int(lat_raw[:2])
                lat_min = float(lat_raw[2:])
                lat = lat_deg + (lat_min / 60)
                if lat_dir == "S":
                    lat *= -1

                lon_deg = int(lon_raw[:3])
                lon_min = float(lon_raw[3:])
                lon = lon_deg + (lon_min / 60)
                if lon_dir == "W":
                    lon *= -1

                return lat, lon
        except:
            pass
        return None