import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QGridLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QKeyEvent

from backupCamWidget import BackupCamWidget
from laneWarnWidget import LaneWarnWidget
from mapWidget import MapWidget
from signWidget import SignWidget

from laneDetection import LaneDetection

from frameProviderThread import FrameProviderThread
from modelSignThread import ModelSignThread
from gpsThread import GPSThread



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



        # Kamera ve model
        self.front_provider = FrameProviderThread(0)
        self.rear_provider = FrameProviderThread(1)
        self.model_sign = ModelSignThread("models/best.pt")

        # Harita
        self.harita_widget = MapWidget()
        self.harita_widget.update_gps(40.7880556,29.4569444)
        self.main_layout.addWidget(self.harita_widget, 0, 0, 3, 3)

        # Geri görüş
        self.geri_gorus_widget = BackupCamWidget(self.rear_provider)
        # self.geri_gorus_widget.start_camera()
        self.main_layout.addWidget(self.geri_gorus_widget, 0, 3, 3, 3)

        # Şerit uyarı
        self.serit_widget = LaneWarnWidget()
        self.lane_detection = LaneDetection()
        # self.serit_widget.check_lane_position(30)  # Sol şeride yaklaşma
        self.serit_widget.show()
        self.main_layout.addWidget(self.serit_widget, 3, 0, 2, 3)

        # Tabela widget
        self.tabela_widget = SignWidget()
        self.main_layout.addWidget(self.tabela_widget, 3, 3, 2, 3)

        

        # Connect
        self.front_provider.frame_ready.connect(self.model_sign.update_frame)
        self.model_sign.result_ready.connect(self.handle_signs)

        self.front_provider.frame_ready.connect(self.handle_lane_warning)

        # self.gps_thread = GPSThread()
        # self.gps_thread.konum_guncelle.connect(self.harita_widget.update_gps)
        # self.gps_thread.start()


        self.front_provider.start()
        self.model_sign.start()
        

        #geri vites
        # self.rear_provider.start()

    



    def handle_lane_warning(self, frame):
        warning = self.lane_detection.process_frame(frame)
        self.serit_widget.uyari_label.setText(warning)
        

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


    def closeEvent(self, event):
        self.front_provider.stop()
        # self.rear_provider.stop()
        self.model_sign.stop()
        super().closeEvent(event)





def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
