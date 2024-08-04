import cv2
import mediapipe

capture_hands = mediapipe.solutions.hands.Hands(max_num_hands=2)
drawing_options = mediapipe.solutions.drawing_utils
camera = cv2.VideoCapture(0)

x1, y1, x2, y2 = 0, 0, 0, 0

while True:
    _, image = camera.read()
    image_height, image_width,_ = image.shape
    image = cv2.flip(image, 1)
    rgb_imiage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output_hands = capture_hands.process(rgb_imiage)
    
    all_hands = output_hands.multi_hand_landmarks
    if all_hands:
        for hand in all_hands:
            drawing_options.draw_landmarks(image, hand, mediapipe.solutions.hands.HAND_CONNECTIONS)
            one_hand_landmarks = hand.landmark
            for id, lm in enumerate(one_hand_landmarks):
                x = int(lm.x * 100)
                y = int(lm.y * 100)
                z = int(lm.z * 100)
                print(f"{id=} {x=} {y=} {z=}\n")

    cv2.imshow("Hand movement video capture", image)
    key = cv2.waitKey(1)
    if key == 27:
        break
    
camera.release()
cv2.destroyAllWindows()