import cv2
from cvzone.HandTrackingModule import HandDetector
import socket

# Parameters
width, height = 1280, 720

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Hand Detector
detector = HandDetector(maxHands=1, detectionCon=0.8)

# Data Send
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

while True:
    # Get frames from webcam
    success, img = cap.read()
    
    # Hands
    hands, img = detector.findHands(img=img)
    data = []
    # Landmark Values = (x, y, z) * 21
    if hands:
        # Get the first hand detected 
        hand = hands[0]
        lmList = hand['lmList']
        # print(f"{lmList=}\n")
        # print(f"{hand=}\n")
        for lm in lmList:
            data.extend([lm[0], height - lm[1], lm[2]])
        # print(f"{data=}\n")
        sock.sendto(str.encode(str(data)), serverAddressPort)
    
    img = cv2.resize(img, (0,0), None, 0.5, 0.5)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27: break


cap.release()
cv2.destroyAllWindows()