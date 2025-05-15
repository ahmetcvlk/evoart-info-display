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
        self.baslik = QLabel("Tespit Edilen Son 3 Tabela")
        self.baslik.setAlignment(Qt.AlignCenter)
        self.baslik.setStyleSheet(
            "font-weight: bold; font-size: 20px; color: white")
        self.layout.addWidget(self.baslik, stretch=1)

        # Tabelalar için grid layout
        self.grid = QGridLayout()
        self.layout.addLayout(self.grid, stretch=3)

        # Siyah arka plan
        self.setStyleSheet(
            "background-color: black; color: white; border-radius: 10px")

        # Listeyi başlatıyoruz
        self.tabela_listesi = []
        self.tabela_paths = []    # Aynı sırada path listesi tutacağız

        # Sonraki tabelalar burada eklenecek
        self.tabela_labels = []

    def yeni_tabela_ekle(self, tabela_resmi_path):
        """Yeni tabela ekler ve yalnızca son 3 tabelayı gösterir"""

        # Zaten varsa tekrar ekleme
        if tabela_resmi_path in self.tabela_paths:
            return


        # Resmi yükle
        image = QImage(tabela_resmi_path)
        if image.isNull():
            print(f"Resim yüklenemedi! : {tabela_resmi_path}")
            return

        tabela_pixmap = QPixmap.fromImage(
            image).scaled(130, 130, Qt.KeepAspectRatio)

        # Yeni tabloyu listeye ekle
        self.tabela_listesi.insert(0, tabela_pixmap)
        self.tabela_paths.insert(0, tabela_resmi_path)

        # Listeyi 3 tablo ile sınırlama
        if len(self.tabela_listesi) > 3:
            self.tabela_listesi.pop()
            self.tabela_paths.pop()

        # Ekranda gösterilen label'ları temizle
        for label in self.tabela_labels:
            label.deleteLater()

        # Yeni tabelaları ekle
        self.tabela_labels = []  # Önceki label'ları sıfırlayalım
        for i, tabela in enumerate(self.tabela_listesi):
            tabela_label = QLabel(self)
            tabela_label.setFixedSize(140, 140)  # Sabit kutu boyutu
            tabela_label.setPixmap(tabela)
            tabela_label.setAlignment(Qt.AlignCenter)  # Resmi ortala
            tabela_label.setStyleSheet(
                "background-color: transparent;")  # Griyi kaldır
            self.tabela_labels.append(tabela_label)
            self.grid.addWidget(tabela_label, 0, i, alignment=Qt.AlignCenter)
