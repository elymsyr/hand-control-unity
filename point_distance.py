import cv2
from cvzone.HandTrackingModule import HandDetector
import socket
import time
import math

# Parameters
width, height = 1280, 720

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Hand Detector
detector = HandDetector(maxHands=1, detectionCon=0.8)

# Data Send
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

# Function to calculate distance from camera
def point_cam_dist(point):
    return math.sqrt(point[0]**2 + point[1]**2 + point[2]**2)

prevTime = 0
fps = 0
fpsText = 0
counter = 0

while True:
    counter += 1
    # Get frames from webcam
    success, img = cap.read()   
    
    # Hands
    hands, img = detector.findHands(img=img)
    data = []
    
    if hands:
        # Get the first hand detected 
        hand = hands[0]
        lmList = hand['lmList']
        
        for lm in lmList:
            x, y, z = lm[0], height - lm[1], lm[2]
            dist = point_cam_dist((x, y, z))
            data.extend([x, y, z, dist])
            
            # Display distance next to each point
            cv2.putText(img, f'{dist:.2f}', (x, height - y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
        
        # Send the data
        sock.sendto(str.encode(str(data)), serverAddressPort)
    
    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    if counter % 2 == 0:
        fpsText = fps
        counter = 0
    prevTime = currTime
    
    # Display FPS
    cv2.putText(img, f'{int(fpsText)} FPS', (20, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (0, 196, 255), 2)
    img = cv2.resize(img, (0, 0), None, 0.6, 0.6)
    cv2.imshow("Image", img)
    
    # Exit on ESC key
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()