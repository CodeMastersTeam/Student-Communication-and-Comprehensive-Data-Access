import cv2

camera = 0

source = cv2.VideoCapture(camera)

window_name = "camera"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

while cv2.waitKey(1) != 27:
    _, frame = source.read()
    if not _:
        break
    cv2.imshow(window_name, frame)

source.release()
cv2.destroyWindow(window_name)