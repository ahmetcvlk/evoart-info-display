import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt


class SimpleLinearGPSToPixel:
    def __init__(self, gps_top_left, gps_bottom_right, pixel_top_left, pixel_bottom_right):
        self.lat1, self.lon1 = gps_top_left
        self.lat2, self.lon2 = gps_bottom_right
        self.x1, self.y1 = pixel_top_left
        self.x2, self.y2 = pixel_bottom_right

    def gps_to_pixel(self, lat, lon):
        # Enlem ve boylam oranlarını bul
        lon_ratio = (lon - self.lon1) / (self.lon2 - self.lon1)
        lat_ratio = (lat - self.lat1) / (self.lat2 - self.lat1)

        # X ve Y koordinatlarını hesapla (not: Y ters gider çünkü resimlerde yukarı 0’dır)
        x = self.x1 + lon_ratio * (self.x2 - self.x1)
        y = self.y1 + lat_ratio * (self.y2 - self.y1)
        return round(x), round(y)


# --- PyQt5 arayüz sınıfı ---
class MapWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.map_label = QLabel(self)
        self.map_pixmap = QPixmap("images/main/racemap.png")  # Harita görselini yüklüyoruz
        self.map_label.setPixmap(self.map_pixmap)
        self.layout.addWidget(self.map_label)

        # Lat/Lon bilgisi için label
        self.coord_label = QLabel(self)
        self.coord_label.setStyleSheet(
            "font-size: 18px; color: yellow; background-color: rgba(0,0,0,180); padding: 5px; border-radius: 5px")
        self.coord_label.setMaximumHeight(40)
        self.layout.addWidget(self.coord_label)


        # Harita köşeleri (sadece iki tanesi gerekiyor)
        gps_top_left = (40.7883333, 29.4511111)
        gps_bottom_right = (40.7855555, 29.4577778)

        pixel_top_left = (0, 0)
        pixel_bottom_right = (857, 487)

        # Basit interpolasyon dönüştürücüyü başlat
        self.converter = SimpleLinearGPSToPixel(
            gps_top_left, gps_bottom_right, pixel_top_left, pixel_bottom_right
        )

        # Harita boyutları
        self.map_width = self.map_pixmap.width()
        self.map_height = self.map_pixmap.height()
        print(f"Map size: {self.map_width}x{self.map_height}")

    def gps_to_pixel(self, lat, lon):
        return self.converter.gps_to_pixel(lat, lon)

    def update_gps(self, lat, lon):
        x, y = self.gps_to_pixel(lat, lon)

        print(f"x:{x}, y:{y}")

        # Yeni bir pixmap üzerine GPS noktası çiz
        temp_pixmap = QPixmap(self.map_pixmap)
        painter = QPainter(temp_pixmap)
        painter.setBrush(QColor(255, 0, 0))  # Kırmızı renk
        painter.drawEllipse(x - 7, y - 7, 14, 14)
        painter.end()

        self.map_label.setPixmap(temp_pixmap)

        #Konum label'ını güncelle
        self.coord_label.setText(f"Lat: {lat:.7f}, Lon: {lon:.7f}")
