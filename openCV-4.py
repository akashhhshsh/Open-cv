import cv2
print(cv2.__version__)

row=int(input('How many rows do you want?  '))
column=int(input('How many columns do you want?  '))

width=1280
height=720

cam=cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

while True:
    ignore,frame=cam.read()
    frame=cv2.resize(frame,(int(width/column),int(height/column)))
    for i in range(0,row):
        for j in range(0,column):
            windName='Window'+str(i)+' x '+str(j)
            cv2.imshow(windName,frame)
            cv2.moveWindow(windName,int(width/column)*j,int(height/column+30)*i)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break
cam.release()    
