import cv2

capture = cv2.VideoCapture(0)
while True:
    success, image = capture.read()
    cv2.imshow("imagewindow", image)
    cv2.waitKey(1)
    windowValue = cv2.getWindowProperty("imagewindow", cv2.WND_PROP_VISIBLE)
    if windowValue < 1:
        break
capture.release()
cv2.destroyAllWindows()