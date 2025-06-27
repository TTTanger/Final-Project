import cv2
from ultralytics import YOLO
import time

class PositionCalculator:
    def __init__(self, model_path="yolo11n.pt", camera_id=0, desk_width_cm=25.5, desk_height_cm=20.0):
        # 加载 YOLO 模型
        self.model = YOLO(model_path)
        # 初始化摄像头
        self.cap = cv2.VideoCapture(camera_id)
        # 设置摄像头分辨率
        self.frame_width = 640
        self.frame_height = 480
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)
        # 桌面实际尺寸
        self.desk_width_cm = desk_width_cm
        self.desk_height_cm = desk_height_cm
        # 图像中心
        self.mx = self.frame_width // 2
        self.my = self.frame_height // 2
        # 每像素代表的真实距离（cm）
        self.cm_per_px_x = self.desk_width_cm / self.frame_width
        self.cm_per_px_y = self.desk_height_cm / self.frame_height

    def pixel_to_world(self, u, v):
        x = (u - self.mx) * self.cm_per_px_x
        y = (v - self.my) * self.cm_per_px_y
        return x, y

    def run(self, print_interval=1.0):
        last_print_time = 0
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            results = self.model(frame)
            # 画出原点标记
            cv2.circle(frame, (self.mx, self.my), 6, (0, 0, 255), -1)
            cv2.putText(frame, "Origin (0, 0)", (self.mx + 10, self.my - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            current_time = time.time()
            for box in results[0].boxes.xyxy:
                x1, y1, x2, y2 = map(int, box)
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                wx, wy = self.pixel_to_world(cx, cy)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)
                cv2.putText(frame, f"({wx:.1f}cm, {wy:.1f}cm)", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                if current_time - last_print_time > print_interval:
                    print(f"物体中心像素坐标: ({cx}, {cy})")
                    last_print_time = current_time

            # 显示图像
            cv2.imshow("YOLO Detection with World Coordinates", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC 退出
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def get_one_center(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            results = self.model(frame)
            for box in results[0].boxes.xyxy:
                x1, y1, x2, y2 = map(int, box)
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                self.cap.release()
                return (cx, cy)  # 检测到第一个目标后立即返回
        self.cap.release()
        return None

if __name__ == "__main__":
    calculator = PositionCalculator()
    calculator.run()