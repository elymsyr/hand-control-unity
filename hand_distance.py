import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

# Initialize the camera
cap = cv2.VideoCapture(0)

# Initialize the hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Known width of the hand (in cm)
known_width = 8.0

# Known distance from the camera (in cm)
known_distance = 30.0

# Width of the hand in pixels at the known distance
known_width_in_pixels = None

while True:
    success, img = cap.read()
    if not success:
        break

    # Detect hand
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        bbox = hand['bbox']
        hand_width_in_pixels = bbox[2]
        
        if known_width_in_pixels is None:
            known_width_in_pixels = hand_width_in_pixels

        # Calculate the distance
        distance = (known_width * known_distance) / hand_width_in_pixels
        print(f"Estimated Distance: {distance:.2f} cm")

        # Draw bounding box and distance
        cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 2)
        cv2.putText(img, f"{distance:.2f} cm", (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    # Display the image
    cv2.imshow("Image", img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
