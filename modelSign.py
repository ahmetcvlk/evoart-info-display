from PyQt5.QtCore import QThread, pyqtSignal
from ultralytics import YOLO

class ModelSign(QThread):
    result_ready = pyqtSignal(list)

    def __init__(self, model_path):
        super().__init__()
        self.model = YOLO(model_path)
        self.frame = None

    def update_frame(self, frame):
        self.frame = frame

    def run(self):
        while True:
            if self.frame is not None:
                results = self.model.predict(self.frame, imgsz=640, conf=0.8, verbose=False)
                boxes = results[0].boxes
                class_ids = boxes.cls.tolist()
                self.result_ready.emit(class_ids)
