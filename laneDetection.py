import cv2
import numpy as np


class LaneDetection:
    def __init__(self):
        pass

    def process_frame(self, frame):
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blur, 50, 150)

            height, width = frame.shape[:2]
            mask = np.zeros_like(edges)
            polygon = np.array([[
                (int(width * 0.1), height),
                (int(width * 0.9), height),
                (int(width * 0.55), int(height * 0.6)),
                (int(width * 0.45), int(height * 0.6))
            ]], np.int32)
            cv2.fillPoly(mask, polygon, 255)
            cropped_edges = cv2.bitwise_and(edges, mask)

            lines = cv2.HoughLinesP(cropped_edges, 1, np.pi / 180, 50,
                                    minLineLength=50, maxLineGap=150)

            if lines is None:
                return "Şeritler tespit edilemedi"

            left_lines = []
            right_lines = []

            for line in lines:
                x1, y1, x2, y2 = line[0]
                parameters = np.polyfit((x1, x2), (y1, y2), 1)
                slope = parameters[0]
                intercept = parameters[1]
                if slope < 0:
                    left_lines.append((slope, intercept))
                else:
                    right_lines.append((slope, intercept))

            if not left_lines or not right_lines:
                return "Şeritler tespit edilemedi"

            left_avg = np.average(left_lines, axis=0)
            right_avg = np.average(right_lines, axis=0)

            left_x = int((height - left_avg[1]) / left_avg[0])
            right_x = int((height - right_avg[1]) / right_avg[0])
            lane_center = (left_x + right_x) // 2
            frame_center = width // 2

            deviation = frame_center - lane_center
            threshold = 80

            if deviation > threshold:
                return "Sağ şeride yaklaşıyorsunuz!"
            elif deviation < -threshold:
                return "Sol şeride yaklaşıyorsunuz!"
            else:
                return "Şeritte düzgün ilerliyorsunuz."

        except Exception as e:
            print(f"[Şerit Algılama Hatası] {e}")
            return "Algılama hatası"
