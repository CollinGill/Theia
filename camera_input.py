import cv2

def open() -> None:
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera...")
        exit()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame. Exiting...")
            exit()

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
