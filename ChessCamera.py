import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    raise IOError("Cannot open webcam")

while True:
  _, frame = camera.read()

  cv2.imshow('Video Feed', frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

camera.release()
cv2.destroyAllWindows()

print('done')