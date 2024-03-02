import cv2
import numpy as np
import pickle

print(cv2.__version__)

width=1280
height=720
bright = 180

cam=cv2.VideoCapture(2,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_BRIGHTNESS,bright)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

class mpHands:
    import mediapipe as mp
    def __init__(self,maxHands=2,complexx=1,tol1=.5,tol2=.5):
        self.handsDetect=self.mp.solutions.hands.Hands(False,maxHands,complexx,tol1,tol2)
    def parseLandMarks(self,frame):
        frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results=self.handsDetect.process(frameRGB)
        myHands=[]
        if results.multi_hand_landmarks != None:
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for LandMark in handLandMarks.landmark:
                    myHand.append((int(LandMark.x*width),int(LandMark.y*height)))
                myHands.append(myHand)
        return myHands

def findDistances(myHands):
    distanceMatrix = np.zeros([len(myHands),len(myHands)],dtype='float')
    palmSize = ((((myHands[0][0]-myHands[9][0])**2)+((myHands[0][1]-myHands[9][1])**2))**(1./2.))#Distance between points 0 and 9.
    for row in range(0,len(myHands),1):
        for column in range(0,len(myHands),1):
            distanceMatrix[row][column] = int(((((myHands[row][0]-myHands[column][0])**2)+((myHands[row][1]-myHands[column][1])**2))**(1./2.))/(palmSize))
    return distanceMatrix

def findError(knownGestureMatrix,unknownGestureMatrix,keyPoints):
    error = 0
    for row in keyPoints:
        for column in keyPoints:
            error = error + abs(knownGestureMatrix[row][column]-unknownGestureMatrix[row][column])
            error = int(error)
            #print(error)
    return error

def findGesture(knownGestures,unKnownGesture,keyPoints,tol,gestureNames):
    errorArray = []
    for i in range(0,len(gestureNames),1):
        error = findError(knownGestures[i],unKnownGesture,keyPoints)
        errorArray.append(error)
    errorMin = errorArray[0]
    minIndex = 0
    for i in range(0,len(gestureNames),1):
        if (errorMin>=errorArray[i]):
            errorMin = errorArray[i]
            minIndex = i
    gesture = 'UNKNOWN'
    if(errorMin<=tol):
        gesture = gestureNames[minIndex]
        #print(errorMin)
    return gesture

findHands=mpHands(1)

keyPoints = [0,4,8,12,16,20,5,9,13,17]
tol = 15

cv2.waitKey(1000)
train=input('Press 1 to Train a Model, Press 0 to Recognize Model ') #input() always returns string
train=int(train)

if train==1:
    knownGestures = []
    gestureNames = []
    c=0
    fileName=input('Enter FileName to store Training Data, (Press Enter for Default FileName) ')
    if(fileName==''):
        fileName='HandTrainingData'
    fileName=fileName+'.pkl' # So it would finally be HandTrainingData.pkl
    print('How many Gestures do you want??')
    k=input()
    k=int(k)

    for i in range(0,k,1):
        print('Enter Gesture Name #'+str(i+1))
        x = input()
        gestureNames.append(x)

if train==0:
    fileName=input('Which Training Data File do you want to use ??, (Press Enter for Default FileName) ')
    if(fileName==''):
        fileName='HandTrainingData'
    fileName=fileName+'.pkl'
    with open(fileName,'rb') as f:
        gestureNames = pickle.load(f)
        knownGestures = pickle.load(f)

while True:
    ignore,frame=cam.read()
    myHands=findHands.parseLandMarks(frame)
    if (train == 1):
        if(myHands != []):
            if (c<k):
                print('Press t to train your Model :',gestureNames[c],'when Ready')
                if (cv2.waitKey(1) & 0xff == ord('t')):
                    oneHand = myHands[0]
                    knownGesture = findDistances(oneHand)
                    knownGestures.append(knownGesture)
                    c=c+1
                
            if (c==k):
                with open(fileName,'wb') as f:
                    pickle.dump(gestureNames,f)
                    pickle.dump(knownGestures,f)
                train = 0

    if (train == 0):
        if (len(myHands) != 0):
            oneHand = myHands[0]
            unknownGesture = findDistances(oneHand)
            gesture = findGesture(knownGestures,unknownGesture,keyPoints,tol,gestureNames)
            cv2.putText(frame,gesture,(100,100),cv2.FONT_HERSHEY_SIMPLEX,4,(0,0,255),3)

    for oneHand in myHands:
        for fingerTip in keyPoints:
            cv2.circle(frame,oneHand[fingerTip],10,(255,255,255),2)

    cv2.imshow('my WEBcam',frame)
    cv2.moveWindow('my WEBcam',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()    
