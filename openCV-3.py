import cv2
print(cv2.__version__)

width=640
height=360

cam=cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

while True:
    ignore,frame=cam.read()
    #frame=cv2.resize(frame,(640,360))
    cv2.imshow('my Cam',frame)
    cv2.moveWindow('my Cam',0,-200)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break
cam.release()    
cv2.destroyAllWindows()