



import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt

# --- Affine dönüşüm sınıfı ---
class AccurateGPSToPixel:
    def __init__(self, gps_points, pixel_points):
        self.gps_matrix = []
        self.pixel_x = []
        self.pixel_y = []

        for (lat, lon), (x, y) in zip(gps_points, pixel_points):
            self.gps_matrix.append([lon, lat, 1])
            self.pixel_x.append(x)
            self.pixel_y.append(y)

        A = np.array(self.gps_matrix)
        bx = np.array(self.pixel_x)
        by = np.array(self.pixel_y)

        self.coeff_x = np.linalg.lstsq(A, bx, rcond=-1.0)[0]
        self.coeff_y = np.linalg.lstsq(A, by, rcond=-1.0)[0]


        # self.coeff_x = np.linalg.lstsq(A, bx, rcond=None)[0]
        # self.coeff_y = np.linalg.lstsq(A, by, rcond=None)[0]

    def gps_to_pixel(self, lat, lon):
        x = self.coeff_x[0] * lon + self.coeff_x[1] * lat + self.coeff_x[2]
        y = self.coeff_y[0] * lon + self.coeff_y[1] * lat + self.coeff_y[2]
        return round(x), round(y)

# --- PyQt5 arayüz sınıfı ---
class MapWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.map_label = QLabel(self)
        self.map_pixmap = QPixmap("images/main/map.png")  # Harita görselini yüklüyoruz
        self.map_label.setPixmap(self.map_pixmap)
        self.layout.addWidget(self.map_label)

        # ➕ Lat/Lon bilgisi için label
        self.coord_label = QLabel(self)
        self.coord_label.setStyleSheet(
            "font-size: 18px; color: yellow; background-color: rgba(0,0,0,180); padding: 5px; border-radius: 5px")
        self.coord_label.setMaximumHeight(40)
        self.layout.addWidget(self.coord_label)

        # Harita köşe koordinatları (decimal degree)
        gps_points = [
            (41.51167, 36.11667),     # sol üst
            (41.50889, 36.11389),     # sağ alt
            (41.5091667, 36.1158333)  # orta nokta
        ]

        pixel_points = [
            (0, 0),        # sol üst
            (821, 486),    # sağ alt
            (661, 140)     # orta noktanın gerçek yeri
        ]

        self.converter = AccurateGPSToPixel(gps_points, pixel_points)

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
        painter.drawEllipse(x - 5, y - 5, 10, 10)
        painter.end()

        self.map_label.setPixmap(temp_pixmap)

         # 🟦 Konum label'ını güncelle
        self.coord_label.setText(f"Lat: {lat:.6f}, Lon: {lon:.6f}")
