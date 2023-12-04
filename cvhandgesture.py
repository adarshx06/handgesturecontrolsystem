import cv2
import os
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Parameters
height,width  = 1000, 1000
folderPath = "C:\\Users\\Adarsh Thoke\\OneDrive\\Desktop\\Computer Vision\\presentation"

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# get the list of presentation image
pathImages = sorted(os.listdir(folderPath),key=len)
#print(pathImages)

#variables for image
imgNumber = 1
#define the video cam
hts, wds = int(120*1),int(150*1)
gestureThreshold = 350
buttonPressed = False
buttonCounter = 0
buttonDelay = 30 #for 10 frams it sonot do any change
annotation = [[]]#for drawing
annotationNumber = 0
annotationStart = False
new_width = 1920
new_height= 1080

cv2.namedWindow("Image", cv2.WINDOW_NORMAL)  # WINDOW_NORMAL allows resizing
cv2.resizeWindow("Image", new_width, new_height)  # Set the new width and height

cv2.namedWindow("Slides", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Slides", new_width, new_height)


#hand detector
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

while True:
# Get image frame
    #Import Image
    success, img = cap.read()
    img = cv2.flip(img,1) #1= horizontal, 0= vertical
    pathFullImage = os.path.join(folderPath,pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)


    hands, img = detectorHand.findHands(img) #flipType= False # to detect hand and display it (fliptype for hand to be in good direction)
    cv2.line(img,(0,gestureThreshold),(width,gestureThreshold),(1, 1, 1, 0), 1) #bgr

    if hands and buttonPressed is False:
        hand = hands[0]
        fingers = detectorHand.fingersUp(hand)
        cx,cy = hand['center']
        lmList = hand['lmList'] #landmarklist
        #constrain for easier pointer movement
        # indexFinger = lmList[8][0], lmList[8][1]
        xVal = int(np.interp(lmList[8][0],[width//2,width],[0,width]))
        yVal = int(np.interp(lmList[8][1],[150,height-150],[0,height]))
        indexFinger = xVal,yVal
        print(fingers)


        if(cy<= gestureThreshold): #to act when its above threshold
            #gesture 1 -left
            if fingers ==[1,0,0,0,0]:
                annotationStart = False
            
                print("Left")
                if imgNumber> 0:
                    buttonPressed = True
                    annotation = [[]]#for drawing
                    annotationNumber = 0

                    imgNumber -=1
                # else:
                #     show("Cannot go Back")

            #gesture 2 -right
            if fingers ==[0,1,1,1,1]:
                annotationStart = False
                print("Right")
                if imgNumber<len(pathImages)-1:
                    buttonPressed = True
                    annotation = [[]]#for drawing
                    annotationNumber = 0
                    
                    imgNumber +=1
            
        #gesture 3 - show pointer
        if fingers ==[0,1,1,0,0]:
            cv2.circle(imgCurrent,indexFinger,5,(0,0,255),cv2.FILLED)
            print("Pointer")

        #gesture 4 - draw pointer
        if fingers ==[0,1,0,0,0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber+=1 
                annotation.append([])
            cv2.circle(imgCurrent,indexFinger,5,(0,0,255),cv2.FILLED)
            annotation[annotationNumber].append(indexFinger)
            print("draw Pointer")
        else:
            annotationStart = False

        #gesture 5 - erase pointer
        if fingers ==[0,1,1,1,0]:
            if annotation:
                if annotationNumber>= 0:

                    annotation.pop(-1)
                    annotationNumber -=1
                    buttonPressed= True
            # cv2.circle(imgCurrent,indexFinger,5,(0,0,255),cv2.FILLED)
            print("Earse Pointer")

    #buttonpressed change to false
    if buttonPressed:
        buttonCounter += 1
        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed =  False

    for i in range (len(annotation)):
        for j in range(len(annotation[i])):
            if(j!=0): 
                cv2.line(imgCurrent,annotation[i][j-1],annotation[i][j],(0,0,255),12)


    # #adding video img on slides
    imgSmall= cv2.resize(img,(wds,hts))
    h,w,_ = imgCurrent.shape
    imgCurrent[h-hts:h,w-wds:w] = imgSmall

    cv2.imshow("Image",img)
    cv2.imshow("Slides", imgCurrent)

    key = cv2.waitKey(1)

    if key== ord('q'):
        break
    # Find the hand and its landmarks
    
# Close all open windows
cv2.destroyAllWindows()





# from cvzone.HandTrackingModule import HandDetector
# import cv2
# import os
# import numpy as np

# # Parameters
# width, height = 1280, 720
# gestureThreshold = 300
# folderPath = "Presentation"

# # Camera Setup
# cap = cv2.VideoCapture(0)
# cap.set(3, width)
# cap.set(4, height)

# # Hand Detector
# detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

# # Variables
# imgList = []
# delay = 30
# buttonPressed = False
# counter = 0
# drawMode = False
# imgNumber = 0
# delayCounter = 0
# annotations = [[]]
# annotationNumber = -1
# annotationStart = False
# hs, ws = int(120 * 1), int(213 * 1)  # width and height of small image

# # Get list of presentation images
# pathImages = sorted(os.listdir(folderPath), key=len)
# print(pathImages)

# while True:
#     # Get image frame
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
#     imgCurrent = cv2.imread(pathFullImage)

#     # Find the hand and its landmarks
#     hands, img = detectorHand.findHands(img)  # with draw
#     # Draw Gesture Threshold line
#     cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

#     if hands and buttonPressed is False:  # If hand is detected

#         hand = hands[0]
#         cx, cy = hand["center"]
#         lmList = hand["lmList"]  # List of 21 Landmark points
#         fingers = detectorHand.fingersUp(hand)  # List of which fingers are up

#         # Constrain values for easier drawing
#         xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
#         yVal = int(np.interp(lmList[8][1], [150, height-150], [0, height]))
#         indexFinger = xVal, yVal

#         if cy <= gestureThreshold:  # If hand is at the height of the face
#             if fingers == [1, 0, 0, 0, 0]:
#                 print("Left")
#                 buttonPressed = True
#                 if imgNumber > 0:
#                     imgNumber -= 1
#                     annotations = [[]]
#                     annotationNumber = -1
#                     annotationStart = False
#             if fingers == [0, 0, 0, 0, 1]:
#                 print("Right")
#                 buttonPressed = True
#                 if imgNumber < len(pathImages) - 1:
#                     imgNumber += 1
#                     annotations = [[]]
#                     annotationNumber = -1
#                     annotationStart = False

#         if fingers == [0, 1, 1, 0, 0]:
#             cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

#         if fingers == [0, 1, 0, 0, 0]:
#             if annotationStart is False:
#                 annotationStart = True
#                 annotationNumber += 1
#                 annotations.append([])
#             print(annotationNumber)
#             annotations[annotationNumber].append(indexFinger)
#             cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

#         else:
#             annotationStart = False

#         if fingers == [0, 1, 1, 1, 0]:
#             if annotations:
#                 annotations.pop(-1)
#                 annotationNumber -= 1
#                 buttonPressed = True

#     else:
#         annotationStart = False

#     if buttonPressed:
#         counter += 1
#         if counter > delay:
#             counter = 0
#             buttonPressed = False

#     for i, annotation in enumerate(annotations):
#         for j in range(len(annotation)):
#             if j != 0:
#                 cv2.line(imgCurrent, annotation[j - 1], annotation[j], (0, 0, 200), 12)

#     imgSmall = cv2.resize(img, (ws, hs))
#     h, w, _ = imgCurrent.shape
#     imgCurrent[0:hs, w - ws: w] = imgSmall

#     cv2.imshow("Slides", imgCurrent)
#     cv2.imshow("Image", img)

#     key = cv2.waitKey(1)
#     if key == ord('q'):
#         break