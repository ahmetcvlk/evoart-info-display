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

# from backupCamThread import BackupCamGpioThread



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

        # Tabela ikonları için sınıf adlarını ve ikon yollarını eşleme
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



        # ----------- Threadler -------- (ön kamera, geri görüş kamerası, tabela model ve GPS)

        # self.front_provider_thread = FrameProviderThread(0)

        # self.backup_cam_gpio_thread = BackupCamGpioThread(gpio_pin=11)
        # self.backup_cam_gpio_thread = BackupCamGpioThread()

        # self.model_sign_thread = ModelSignThread("models/best.pt")

        # self.gps_thread = GPSThread()




        # --------- Widgetlar -----------

        # Harita
        self.harita_widget = MapWidget()
        self.harita_widget.update_gps(40.7866667,29.4550000)  # deneme amaçlı, kaldırılacak
        self.main_layout.addWidget(self.harita_widget, 0, 0, 3, 3)

        # Geri görüş
        self.geri_gorus_widget = BackupCamWidget()
        self.main_layout.addWidget(self.geri_gorus_widget, 0, 3, 3, 3)

        # Şerit uyarı
        self.serit_widget = LaneWarnWidget()
        self.lane_detection = LaneDetection()
        self.main_layout.addWidget(self.serit_widget, 3, 0, 2, 3)

        # Tabela widget
        self.tabela_widget = SignWidget()
        self.main_layout.addWidget(self.tabela_widget, 3, 3, 2, 3)

        

        # --------- Connect ----------

        # self.front_provider_thread.frame_ready.connect(self.model_sign_thread.update_frame) # Ön kamera görüntüsünü tabela modeline gönder
        # self.model_sign_thread.result_ready.connect(self.handle_signs) # Tabela modelinden çıkan sonuçları işleme al

        # self.front_provider_thread.frame_ready.connect(self.handle_lane_warning) # Ön kamera görüntüsünü şerit uyarı modeline gönder

        # self.gps_thread.konum_guncelle.connect(self.harita_widget.update_gps) # GPS konumunu haritada güncelle

        # self.backup_cam_gpio_thread.reverse_changed.connect(self.handle_reverse_gear) # Geri görüş kamerası için geri vites değişimini dinle




        # ----------- Thread Başlatma -----------

        # self.front_provider_thread.start()
        # self.model_sign_thread.start()
        # self.gps_thread.start()
        # self.backup_cam_gpio_thread.start()        




    # --------Fonksiyonlar----------

    # Şerit uyarı mesajını güncelle
    def handle_lane_warning(self, frame):
        warning = self.lane_detection.process_frame(frame)
        self.serit_widget.uyari_label.setText(warning)
        
    # class idlerine göre tabela ekleme
    def handle_signs(self, class_ids):
        for class_id in class_ids:
            try:
                class_name = self.model_sign_thread.model.model.names[int(class_id)]
                print(class_name)
                icon_path = self.class_name_to_icon.get(class_name)
                if icon_path:
                    self.tabela_widget.yeni_tabela_ekle(icon_path)
            except Exception as e:
                print(f"Hata: {e}")

    # Geri görüş kamerası için geri vites değişimini dinleme
    def handle_reverse_gear(self, is_active):
        if is_active:
            print("Geri görüş açıldı")
            self.geri_gorus_widget.start_camera()
        else:
            print("Geri görüş kapandı")
            self.geri_gorus_widget.stop_camera()


    # Pencere kapatıldığında threadleri durdurma
    def closeEvent(self, event):
        # self.front_provider_thread.stop()
        # self.model_sign_thread.stop()
        # self.gps_thread.stop()
        # self.backup_cam_gpio_thread.stop()
        super().closeEvent(event)





def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
