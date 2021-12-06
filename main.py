import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import pyautogui as pyg

SCREENX = pyg.size()[0]
SCREENY = pyg.size()[1]

pTime = 0
cTime = 0

cap = cv2.VideoCapture(0)
detector = htm.handDetector()

while True:
    success, img = cap.read()

    img = cv2.flip(img, 1)
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        c = lmList["0"]
        d = lmList["17"]
        # calculate distance between c and d
        distance2 = ((c[0] - d[0]) ** 2 + (c[1] - d[1]) ** 2) ** 0.5
        # print("A :", distance2)

        a = lmList["4"]
        b = lmList["8"]
        # calculate distance between a and b
        distance = ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
        # print("B :", distance)

        maxX = img.shape[1]
        maxY = img.shape[0]
        facX = 50
        facY = 100
        resX = maxX - facX
        resY = maxY - facY

        #print(maxX, maxY)

        # if distance is less than 1/10 of distance 2, click

        #
        #    ...

        #scale c[0] between (facX/2)) and (resX+(facX/2))
        if c[0] < facX/2:
            c[0] = facX/2
        elif c[0] > resX + (facX / 2):
            c[0] = resX + (facX / 2)

        #scale c[1] between (facY/2)) and (resY+(facY/2))
        if c[1] < facY/2:
            c[1] = facY/2
        elif c[1] > resY + (facY / 2):
            c[1] = resY + (facY / 2)

        if distance < distance2/2:
            pyg.click()
        else:
            x = (c[0] - (facX / 2)) / resX * SCREENX
            y = (c[1] - (facY/2)) / resY * SCREENY
            pyg.moveTo(x, y)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.imshow("Image", img)
    cv2.waitKey(1)
