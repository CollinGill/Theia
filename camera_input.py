import cv2 as cv

# Opens camera and returns capture object
def open() -> cv.VideoCapture:
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera...")
        exit()

    return cap


# Closes camera
def close(capture: cv.VideoCapture) -> None:
    capture.release()
    cv.destroyAllWindows()