from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage
import cv2

class BackupCamWidget(QWidget):
    def __init__(self, frame_provider, parent=None):
        super().__init__(parent)
        self.frame_provider = frame_provider
        self.frame_provider.frame_ready.connect(self.update_frame)
        self.initUI()


        # self.camera_index = 0  # Kamera indeksi (birden fazla kamera varsa değiştirilebilir)
        # self.camera = None
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_frame)
        
    def initUI(self):
        # Widget için layout oluştur
        self.layout = QVBoxLayout(self)
        
        # Kamera görüntüsünü gösterecek label
        self.cameraLabel = QLabel()
        self.cameraLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.cameraLabel,stretch=3)

        self.cam_info_label = QLabel(self)
        self.cam_info_label.setStyleSheet(
            "font-size: 18px; color: yellow; background-color: rgba(0,0,0,180); padding: 10px; border-radius: 5px;")
        self.cam_info_label.setMaximumHeight(40)
        self.cam_info_label.setText("Geri görüş kamerası kapalı.")
        self.layout.addWidget(self.cam_info_label,stretch=0)
        
        
        
        # Widget stilini ayarla
        self.setStyleSheet("background-color: black;")
        self.setMinimumSize(320, 240)
        
    def start_camera(self):
        """FrameProvider başlatılır."""
        if not self.frame_provider.isRunning():
            self.cam_info_label.setText("Geri görüş kamerası açık.")
            self.frame_provider.start()

    
    def stop_camera(self):
        """FrameProvider durdurulur."""
        if self.frame_provider.isRunning():
            self.cam_info_label.setText("Geri görüş kamerası kapalı.")
            self.frame_provider.stop()
    
    def update_frame(self, frame):
        """Yeni gelen kareyi göster."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)

        scaled_pixmap = pixmap.scaled(self.cameraLabel.width(), self.cameraLabel.height(),
                                      Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.cameraLabel.setPixmap(scaled_pixmap)
    
    def resizeEvent(self, event):
        """Widget yeniden boyutlandırıldığında çağrılır"""
        super().resizeEvent(event)
        # Kamera açıksa mevcut kareyi yeniden boyutlandır
        if hasattr(self, 'cameraLabel') and self.cameraLabel.pixmap():
            pixmap = self.cameraLabel.pixmap()
            scaled_pixmap = pixmap.scaled(self.cameraLabel.width(), self.cameraLabel.height(), 
                                         Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.cameraLabel.setPixmap(scaled_pixmap)
    
    def closeEvent(self, event):
        """Widget kapatıldığında kamera kaynaklarını serbest bırak"""
        self.stop_camera()
        super().closeEvent(event)


