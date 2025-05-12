#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage
import cv2

class BackupCamWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.camera_index = 1  # Kamera indeksi (birden fazla kamera varsa değiştirilebilir)
        self.camera = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        
    def initUI(self):
        # Widget için layout oluştur
        self.layout = QVBoxLayout(self)
        
        # Kamera görüntüsünü gösterecek label
        self.cameraLabel = QLabel()
        self.cameraLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.cameraLabel)
        
        
        
        # Widget stilini ayarla
        self.setStyleSheet("background-color: black;")
        self.setMinimumSize(320, 240)
        
    def start_camera(self):
        """Kamera yakalamayı başlat"""
        try:
            self.camera = cv2.VideoCapture(self.camera_index)
            if not self.camera.isOpened():
                return False
                
            self.timer.start(30)  # 30ms - yaklaşık 33 FPS
            return True
        except Exception as e:
            print(f"Kamera başlatma hatası: {e}")
            return False
    
    def stop_camera(self):
        """Kamera yakalamayı durdur"""
        if self.timer.isActive():
            self.timer.stop()
        if self.camera is not None and self.camera.isOpened():
            self.camera.release()
    
    def update_frame(self):
        """Kameradan yeni kare al ve göster"""
        if self.camera is None or not self.camera.isOpened():
            return
        
        ret, frame = self.camera.read()
        if not ret:
            self.stop_camera()
            return
        
        # OpenCV BGR formatından Qt QImage formatına dönüştür
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        
        q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        
        # Label'a ölçeklendirilmiş olarak yerleştir
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


# Test için
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    widget = BackupCamWidget()
    widget.show()
    
    # Kamerayı başlat
    success = widget.start_camera()
    if not success:
        print("Kamera başlatılamadı. Lütfen kamera bağlantısını kontrol edin.")
    
    sys.exit(app.exec_())