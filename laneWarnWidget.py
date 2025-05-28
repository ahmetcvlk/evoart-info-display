import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage


class LaneWarnWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Başlık
        self.baslik = QLabel("Şerit ve Kör Nokta Uyarısı")
        self.baslik.setAlignment(Qt.AlignCenter)
        self.baslik.setStyleSheet(
            "font-weight: bold; font-size: 20px; color: white")
        self.layout.addWidget(self.baslik, stretch=1)

        # Uyarı mesajları için QLabel
        self.uyari_label = QLabel("Şu anda şeritte değilsiniz.")
        self.uyari_label.setAlignment(Qt.AlignCenter)
        self.uyari_label.setStyleSheet(
            "font-size: 20px; color: yellow; background-color: rgba(0,0,0,180); padding: 5px; border-radius: 5px")
        self.layout.addWidget(self.uyari_label, stretch=3)

        # Uyarı mesajları için QLabel
        self.kor_nokta_label = QLabel("Kök noktalar boş.")
        self.kor_nokta_label.setAlignment(Qt.AlignCenter)
        self.kor_nokta_label.setStyleSheet(
            "font-size: 20px; color: yellow; background-color: rgba(0,0,0,180); padding: 5px; border-radius: 5px")
        self.layout.addWidget(self.kor_nokta_label, stretch=3)

        # Siyah arka plan
        self.setStyleSheet(
            "background-color: black; color: white; border-radius: 10px")

    def set_warning_message(self, direction):
        """Şeride yaklaşma durumuna göre uyarı mesajını ayarlama"""
        if direction == "right":
            self.uyari_label.setText("Sağ şeride yaklaşıyorsunuz!")
            self.uyari_label.setStyleSheet(
                "font-size: 25px; color: red; background-color: rgba(0,0,0,180); padding: 5px; border-radius: 5px")
        elif direction == "left":
            self.uyari_label.setText("Sol şeride yaklaşıyorsunuz!")
            self.uyari_label.setStyleSheet(
                "font-size: 25px; color: red; background-color: rgba(0,0,0,180); padding: 5px; border-radius: 5px")
        else:
            self.uyari_label.setText("Şu anda şeritte değilsiniz.")
            self.uyari_label.setStyleSheet(
                "font-size: 16px; color: yellow; background-color: rgba(0,0,0,180); padding: 5px; border-radius: 5px")

    def check_lane_position(self, position):
        """Pozisyona göre şeritteki konum kontrolü"""
        # Sol ve sağ şeride yakınlık için threshold değerleri
        # Bu değerler kameradan veya sensörden gelen verilere göre ayarlanabilir.
        if position < 50:
            self.set_warning_message("left")  # Sol şeride yaklaşma
        elif position > 950:  # Harita boyutları veya ekran genişliği üzerinden sınır belirlenebilir
            self.set_warning_message("right")  # Sağ şeride yaklaşma
        else:
            self.set_warning_message("center")  # Şerit içinde normal konum
