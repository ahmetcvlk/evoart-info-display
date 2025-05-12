import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage

class SignWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Başlık
        self.baslik = QLabel("Son 3 Tabela")
        self.baslik.setAlignment(Qt.AlignCenter)
        self.baslik.setStyleSheet(
            "font-weight: bold; font-size: 14px; color: white")
        self.layout.addWidget(self.baslik)

        # Tabelalar için grid layout
        self.grid = QGridLayout()
        self.layout.addLayout(self.grid)

        # Siyah arka plan
        self.setStyleSheet(
            "background-color: black; color: white; border-radius: 10px")

        # Listeyi başlatıyoruz
        self.tabela_listesi = []

        # Sonraki tabelalar burada eklenecek
        self.tabela_labels = []

    def yeni_tabela_ekle(self, tabela_resmi_path):
        """Yeni tabela ekler ve yalnızca son 3 tabelayı gösterir"""
        # Resmi yükle
        image = QImage(tabela_resmi_path)
        if image.isNull():
            print("Resim yüklenemedi!")
            return

        tabela_pixmap = QPixmap.fromImage(image).scaled(80, 80, Qt.KeepAspectRatio)

        # Yeni tabloyu listeye ekle
        self.tabela_listesi.append(tabela_pixmap)

        # Listeyi 3 tablo ile sınırlama
        if len(self.tabela_listesi) > 3:
            self.tabela_listesi.pop(0)

        # Ekranda gösterilen label'ları temizle
        for label in self.tabela_labels:
            label.deleteLater()

        # Yeni tabelaları ekle
        self.tabela_labels = []  # Önceki label'ları sıfırlayalım
        for i, tabela in enumerate(self.tabela_listesi):
            tabela_label = QLabel(self)
            tabela_label.setPixmap(tabela)
            self.tabela_labels.append(tabela_label)
            self.grid.addWidget(tabela_label, 0, i)

