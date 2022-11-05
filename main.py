import cv2 as cv
import camera_input

def main():
    capture = camera_input.open()

    cv.namedWindow("Theia", cv.WINDOW_NORMAL)
    
    while True:
        ret, frame = capture.read()
        if not ret:
            print("Cannot read frame...")
            break

        cv.setWindowProperty("Theia", cv.WND_PROP_FULLSCREEN, cv.WND_PROP_FULLSCREEN)
        cv.imshow("Theia", frame)

        if cv.waitKey(1) == ord('q') or cv.getWindowProperty("Theia", cv.WND_PROP_VISIBLE) < 1:
            break
    
    camera_input.close(capture)

if __name__ == '__main__':
    main()