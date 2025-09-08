import cv2
import mediapipe as mp
import numpy as np
import joblib
import pyautogui
import time


MODEL_PATH = 'final_model_v2_svm (1).pkl'

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    print(f"Error: Model file '{MODEL_PATH}' not found.")
    print("Please ensure the model file is in the same directory as the script.")
    exit()

GESTURE_MAP = {
    0: "Rewind",
    1: "Fast Forward",
    2: "Play/Pause",
    3: "Volume Down",
    4: "Volume Up"
}

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6
)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

video_is_playing = False
last_action_time = 0
ACTION_DELAY = 1.0 

print("Hand gesture control system is ready. Press 'q' to quit.")
print("Start by showing the 'Stop' gesture to play the video.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(img_rgb)
    action_text = ""

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

            landmarks_for_model = np.array(landmarks).reshape(1, -1)
            pred_class = model.predict(landmarks_for_model)[0]
            action_name = GESTURE_MAP.get(pred_class, "Unknown")

            action_text = f"Action: {action_name}"

            current_time = time.time()
            if current_time - last_action_time > ACTION_DELAY:
                if action_name == "Play/Pause":
                    pyautogui.press('space')
                    video_is_playing = not video_is_playing
                    print(f"Action: Play/Pause -> Video state is now {'Playing' if video_is_playing else 'Paused'}")
                    last_action_time = current_time

                elif video_is_playing:
                    if action_name == "Fast Forward":
                        pyautogui.press('right')
                        print("Action: Fast Forward")
                        last_action_time = current_time
                    elif action_name == "Rewind":
                        pyautogui.press('left')
                        print("Action: Rewind")
                        last_action_time = current_time
                    elif action_name == "Volume Up":
                        pyautogui.press('up')
                        print("Action: Volume Up")
                        last_action_time = current_time
                    elif action_name == "Volume Down":
                        pyautogui.press('down')
                        print("Action: Volume Down")
                        last_action_time = current_time

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    state_text = f"State: {'Playing' if video_is_playing else 'Paused'}"
    cv2.putText(frame, state_text, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.putText(frame, action_text, (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Hand Gesture Control', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
print("Program terminated.")
