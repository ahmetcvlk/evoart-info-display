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
        self.uyari_label = QLabel("Şeritler tespit edilemedi")
        self.uyari_label.setAlignment(Qt.AlignCenter)
        self.uyari_label.setStyleSheet(
            "font-size: 20px; color: yellow; background-color: rgba(0,0,0,180); padding: 5px; border-radius: 5px")
        self.layout.addWidget(self.uyari_label, stretch=3)

        # Kör nokta uyarısı için QLabel
        self.kor_nokta_label = QLabel("Kör noktalar boş")
        self.kor_nokta_label.setAlignment(Qt.AlignCenter)
        self.kor_nokta_label.setStyleSheet(
            "font-size: 20px; color: yellow; background-color: rgba(0,0,0,180); padding: 5px; border-radius: 5px")
        self.layout.addWidget(self.kor_nokta_label, stretch=3)

        # Siyah arka plan
        self.setStyleSheet(
            "background-color: black; color: white; border-radius: 10px")

