from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage
from frameProviderThread import FrameProviderThread
import cv2


class BackupCamWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.frame_provider = FrameProviderThread(1)
        self.frame_provider.frame_ready.connect(self.update_frame)
        self.active = False  # Başlangıçta kamera pasif
        self.frame_provider.start()  # Thread bir kez başlatılıyor

        self.initUI()

    def initUI(self):
        # Widget için layout oluştur
        self.layout = QVBoxLayout(self)

        # Kamera görüntüsünü gösterecek label
        self.cameraLabel = QLabel()
        self.cameraLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.cameraLabel, stretch=3)

        self.cam_info_label = QLabel(self)
        self.cam_info_label.setStyleSheet(
            "font-size: 18px; color: yellow; background-color: rgba(0,0,0,180); padding: 10px; border-radius: 5px;")
        self.cam_info_label.setMaximumHeight(40)
        self.cam_info_label.setText("Geri görüş kamerası kapalı.")
        self.layout.addWidget(self.cam_info_label, stretch=0)

        # Widget stilini ayarla
        self.setStyleSheet("background-color: black;")
        self.setMinimumSize(320, 240)



    def start_camera(self):
        self.active = True
        self.cam_info_label.setText("Geri görüş kamerası açık.")

    def stop_camera(self):
        self.active = False
        self.cam_info_label.setText("Geri görüş kamerası kapalı.")
        # Siyah ekran göster
        black_pixmap = QPixmap(self.cameraLabel.size())
        black_pixmap.fill(Qt.black)
        self.cameraLabel.setPixmap(black_pixmap)

    

    def update_frame(self, frame):
        if not self.active:
            return  # Kamera pasifse kareleri yoksay
        
        """Yeni gelen kareyi göster."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_frame.data, w, h,
                       bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)

        scaled_pixmap = pixmap.scaled(self.cameraLabel.size(),
                                      Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.cameraLabel.setPixmap(scaled_pixmap)
