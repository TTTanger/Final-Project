import cv2
from ultralytics import YOLO
import time

# 加载 YOLO 模型（可换成你的自训练模型）
model = YOLO("yolo11n.pt")

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 设置摄像头分辨率（确保为640x480）
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 实际桌面尺寸（单位：cm） —— 你要测量桌面实际视野
desk_width_cm =  25.5  # 左右方向的宽度
desk_height_cm = 20.0       # 上下方向的长度（相机视野前后方向）

# 图像分辨率
frame_width = 640
frame_height = 480

# 图像中心像素坐标 = 世界坐标原点
mx = frame_width // 2
my = frame_height // 2

# 每像素代表的真实距离（cm）
cm_per_px_x = desk_width_cm / frame_width
cm_per_px_y = desk_height_cm / frame_height

# 像素坐标 → 世界坐标（以图像中心为原点）
def pixel_to_world(u, v):
    x = (u - mx) * cm_per_px_x
    y = (v - my) * cm_per_px_y
    return x, y

last_print_time = 0
print_interval = 0.5  # 每0.5秒输出一次

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 运行 YOLO 检测
    results = model(frame)

    # 画出原点标记（图像中心）
    cv2.circle(frame, (mx, my), 6, (0, 0, 255), -1)  # 红色实心圆
    cv2.putText(frame, "Origin (0, 0)", (mx + 10, my - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    current_time = time.time()
    # 遍历检测结果
    for box in results[0].boxes.xyxy:
        x1, y1, x2, y2 = map(int, box)
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # 坐标转换
        wx, wy = pixel_to_world(cx, cy)

        # 画检测框 + 中心 + 坐标文字
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)  # 蓝色中心点
        cv2.putText(frame, f"({wx:.1f}cm, {wy:.1f}cm)", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # 降低输出频率，只每隔 print_interval 秒输出一次
        if current_time - last_print_time > print_interval:
            print(f"物体中心像素坐标: ({cx}, {cy})")
            last_print_time = current_time

    # 显示图像
    cv2.imshow("YOLO Detection with World Coordinates", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC 退出
        break

cap.release()
cv2.destroyAllWindows()