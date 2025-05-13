import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt

class MapWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        self.map_label = QLabel(self)
        self.map_pixmap = QPixmap("traffic-signs\map.png")  # Harita görselini yüklüyoruz
        self.map_label.setPixmap(self.map_pixmap)
        self.layout.addWidget(self.map_label)

     


        # Harita köşe koordinatları (decimal degree)
        self.lat1, self.lon1 = 41.51167, 36.11667  # sol üst (enlem, boylam)
        self.lat2, self.lon2 = 41.50889, 36.11389  # sağ alt (enlem, boylam)

        # Harita boyutları
        self.map_width = self.map_pixmap.width()   # 821 px
        print(self.map_width)
        self.map_height = self.map_pixmap.height()  # 486 px
        print(self.map_height)

    def gps_to_pixel(self, lat, lon):
        # Latitude (N) ters orantılı → X ekseni
        lat_span = self.lat1 - self.lat2  # enlem farkı
        x = ((self.lat1 - lat) / lat_span) * self.map_width

        # Longitude (E) ters orantılı → Y ekseni
        lon_span = self.lon1 - self.lon2  # boylam farkı
        y = ((self.lon1 - lon) / lon_span) * self.map_height

        return int(round(x)), int(round(y))









    def update_gps(self, lat, lon):
        x, y = self.gps_to_pixel(lat, lon)

        print(f"x:{x}, y:{y}")

        # Yeni bir pixmap üzerine GPS noktası çiz
        temp_pixmap = QPixmap(self.map_pixmap)
        painter = QPainter(temp_pixmap)
        painter.setBrush(QColor(255, 0, 0))  # Kırmızı renk
        painter.drawEllipse(x - 5, y - 5, 10, 10)  # GPS noktasının etrafında bir daire çizeceğiz
        painter.end()

        self.map_label.setPixmap(temp_pixmap)

