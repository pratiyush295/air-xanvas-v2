import cv2
import numpy as np
import mediapipe as mp

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Variables
draw = False
erase = False
selected_color = (0, 0, 255)  # Default to red color
canvas = np.ones((480, 640, 3), np.uint8) * 255

# Function to draw color selection boxes
def draw_rect(img):
    cv2.rectangle(img, (20, 5), (100, 60), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, "ERASE ALL", (30, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
    cv2.rectangle(img, (130, 5), (210, 60), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, "ERASER", (140, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
    cv2.rectangle(img, (240, 5), (320, 60), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, "GREEN", (250, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1)
    cv2.rectangle(img, (350, 5), (430, 60), (0, 0, 255), cv2.FILLED)
    cv2.putText(img, "RED", (360, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1)
    cv2.rectangle(img, (470, 5), (550, 60), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, "BLUE", (480, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 0), 1)

# Logic for erasing and drawing based on finger-tip/thumb positions
def detect_draw_or_erase(landmarks):
    global draw, erase
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    if index_tip.visibility > 0.5 and thumb_tip.visibility < 0.5:
        draw = True
        erase = False
    elif thumb_tip.visibility > 0.5 and index_tip.visibility < 0.5:
        erase = True
        draw = False
    else:
        draw = False
        erase = False  # When both are close together, stop both actions

# Main execution
mode_choice = input("Choose mode: 'object' or 'finger' ")

if mode_choice == "object":
    # Object detection code goes here (from your previous object detection implementation)
    pass
elif mode_choice == "finger":
    video = cv2.VideoCapture(0)

    while True:
        _, img = video.read()
        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(img_rgb)

        draw_rect(img)  # Draw the UI boxes

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Detect thumb and fingertip positions for erasing/drawing
                detect_draw_or_erase(hand_landmarks.landmark)
                
                # Get the index finger tip position for drawing
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                h, w, _ = img.shape
                cx, cy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

                if draw:
                    cv2.circle(canvas, (cx, cy), 8, selected_color, cv2.FILLED)
                elif erase:
                    cv2.circle(canvas, (cx, cy), 24, (255, 255, 255), cv2.FILLED)

        # Display the combined image with the canvas
        combined = cv2.addWeighted(img, 0.5, canvas, 0.5, 0)
        cv2.imshow("Canvas", combined)

        key = cv2.waitKey(1)
        if key == ord("q"):  # Press 'q' to quit
            break

    video.release()
    cv2.destroyAllWindows()
