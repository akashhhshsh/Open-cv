import cv2

frameWidth = 640
frameHeight = 480
cam = cv2.VideoCapture(0)
cam.set(3, frameWidth)
cam.set(4, frameHeight)
cam.set(10,150)

while True:
    ignore, frame = cam.read()
    grayframe=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.imshow('my Webcam',frame)
    cv2.moveWindow('my Webcam',0,-200)
    cv2.imshow('my gray',grayframe)
    cv2.moveWindow('my gray',640,-200)
    cv2.imshow('my Webcam2',frame)
    cv2.moveWindow('my Webcam2',640,280)
    cv2.imshow('my gray2',grayframe) 
    cv2.moveWindow('my gray2',0,280)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break
cam.release()