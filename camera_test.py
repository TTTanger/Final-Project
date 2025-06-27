import cv2

def list_cameras():
    # Try camera indices from 0 to 9
    available_cameras = []
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                available_cameras.append(i)
                print(f"Camera {i} is available")
            cap.release()
        else:
            print(f"Camera {i} is not available")
    
    return available_cameras

if __name__ == "__main__":
    print("Testing available cameras...")
    cameras = list_cameras()
    print(f"\nAvailable cameras: {cameras}")