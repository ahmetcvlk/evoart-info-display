import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QGridLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QKeyEvent

from backupCamWidget import BackupCamWidget
from laneWarnWidget import LaneWarnWidget
from mapWidget import MapWidget
from signWidget import SignWidget

from frameProvider import FrameProvider
from modelSign import ModelSign


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

        self.class_name_to_icon = {
            "no_entry": "images/traffic-signs/no_entry.png",
            "forward_and_left": "images/traffic-signs/forward_and_left.png",
            "forward_and_right": "images/traffic-signs/forward_and_right.png",
            "mandatory_left": "images/traffic-signs/mandatory_left.png",
            "mandatory_right": "images/traffic-signs/mandatory_right.png",
            "no_right_turn": "images/traffic-signs/no_right_turn.png",
            "no_left_turn": "images/traffic-signs/no_left_turn.png",
            "red_light": "images/traffic-signs/red_light.png",
            "green_light": "images/traffic-signs/green_light.png",
            "station": "images/traffic-signs/station.png",
            "park": "images/traffic-signs/park.png",
            "no_park": "images/traffic-signs/no_park.png",
            "intersection": "images/traffic-signs/intersection.png",
            "handicapped_parking": "images/traffic-signs/handicapped_parking.jpg"
        }

        # Harita
        self.harita_widget = MapWidget()
        self.harita_widget.update_gps(41.50944, 36.115)
        self.main_layout.addWidget(self.harita_widget, 0, 0, 3, 3)

        # Geri görüş
        self.geri_gorus_widget = BackupCamWidget()
        # self.geri_gorus_widget.start_camera()
        self.main_layout.addWidget(self.geri_gorus_widget, 0, 3, 3, 3)

        # Şerit uyarı
        self.serit_widget = LaneWarnWidget()
        self.serit_widget.check_lane_position(30)  # Sol şeride yaklaşma
        self.serit_widget.show()
        self.main_layout.addWidget(self.serit_widget, 3, 0, 2, 3)

        # Tabela widget
        self.tabela_widget = SignWidget()
        self.main_layout.addWidget(self.tabela_widget, 3, 3, 2, 3)

        # Kamera ve model
        self.frame_provider = FrameProvider()
        self.model_sign = ModelSign("models/best.pt")

        self.frame_provider.frame_ready.connect(self.model_sign.update_frame)
        self.model_sign.result_ready.connect(self.handle_signs)

        self.frame_provider.start()
        self.model_sign.start()

    def handle_signs(self, class_ids):
        for class_id in class_ids:
            try:
                class_name = self.model_sign.model.model.names[int(class_id)]
                print(class_name)
                icon_path = self.class_name_to_icon.get(class_name)
                if icon_path:
                    self.tabela_widget.yeni_tabela_ekle(icon_path)
            except Exception as e:
                print(f"Hata: {e}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
