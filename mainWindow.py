import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QGridLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage,QPixmap,QKeyEvent

from backupCamWidget import BackupCamWidget
from laneWarnWidget import LaneWarnWidget
from mapWidget import MapWidget
from signWidget import SignWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Araç Arayüzü")
        self.setGeometry(200, 90, 1600, 900)
        self.setStyleSheet("background-color: #262626;")

        # Ana widget ve layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QGridLayout()
        self.central_widget.setLayout(self.main_layout)

        self.harita_widget = MapWidget()
        self.harita_widget.update_gps(41.50944, 36.115)
        self.main_layout.addWidget(self.harita_widget, 0, 0, 3, 3)
        

        self.geri_gorus_widget = BackupCamWidget()
        self.geri_gorus_widget.start_camera()
        self.main_layout.addWidget(self.geri_gorus_widget, 0, 3, 3, 3)

        self.serit_widget = LaneWarnWidget()
        self.serit_widget.check_lane_position(30)  # Sol şeride yaklaşma
        self.serit_widget.show()
        self.main_layout.addWidget(self.serit_widget, 3, 0, 2, 3)

        self.tabela_widget = SignWidget()
        self.tabela_widget.yeni_tabela_ekle("traffic-signs//dur.png")  # Bu resimleri güncel yol ile değiştirin
        self.tabela_widget.yeni_tabela_ekle("traffic-signs//yayagecidi.png")
        self.tabela_widget.yeni_tabela_ekle("traffic-signs//yesilisik.jpeg")
        self.main_layout.addWidget(self.tabela_widget, 3, 3, 2, 3)








def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

