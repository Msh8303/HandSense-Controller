import cv2
import mediapipe as mp
import numpy as np
import joblib
import time
from gpiozero import LED 
from signal import pause
import sys

LED_PINS = [17, 18, 22, 23, 24] 
try:
    leds = [LED(pin) for pin in LED_PINS]
except Exception as e:
    print(f"Error initializing GPIO pins: {e}")
    print("Please ensure you are running this script on a Raspberry Pi and have the correct permissions.")
    sys.exit()


is_low_light = True

try:
    model = joblib.load('final_model_v2_svm (1).pkl')
    print("Model loaded successfully.")
except FileNotFoundError:
    print("Error: Model file 'final_model_v2_svm (1).pkl' not found.")
    print("Please ensure the model file is in the same directory as the script.")
    sys.exit()

GESTURE_MAP = {
    0: "Left Swipe",
    1: "Right Swipe",
    2: "Stop",
    3: "Thumbs Down",
    4: "Thumbs Up"
}

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320); cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

system_is_on = False
last_action_time = 0
ACTION_DELAY = 2.0  
def get_swipe_pattern(direction):
    """Returns a list of boolean lists for the swipe animation."""
    if direction == 'left':
        return [
            [True, True, True, True, False],
            [True, True, True, False, True],
            [True, True, False, True, True],
            [True, False, True, True, True],
            [False, True, True, True, True],
        ]
    else:  
        return [
            [False, True, True, True, True],
            [True, False, True, True, True],
            [True, True, False, True, True],
            [True, True, True, False, True],
            [True, True, True, True, False],
        ]

def extract_landmarks_for_model(hand_landmarks):
    """Extracts landmarks and prepares them for the model."""
    landmarks = []
    for lm in hand_landmarks.landmark:
        landmarks.extend([lm.x, lm.y, lm.z])
    return np.array(landmarks).reshape(1, -1)


print("Hand gesture LED control system is ready. Press 'q' on the OpenCV window to quit.")
print("Start by showing the 'Stop' gesture to turn all LEDs OFF.")
print("Show the 'Thumbs Up' gesture to turn them on with low light.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    action_text = ""
    gesture_recognized = "None"
    
    current_time = time.time()
    
    if result.multi_hand_landmarks:
        if current_time - last_action_time > ACTION_DELAY:
            hand_landmarks = result.multi_hand_landmarks[0]
            landmarks_for_model = extract_landmarks_for_model(hand_landmarks)
            
            pred_class = model.predict(landmarks_for_model)[0]
            gesture_recognized = GESTURE_MAP.get(pred_class, "Unknown")
            action_text = f"Action: {gesture_recognized}"

            if gesture_recognized == "Stop":
                for led in leds:
                    led.off()
                system_is_on = False
                print("Action: All LEDs OFF.")
                last_action_time = current_time

            elif gesture_recognized == "Thumbs Up" and not system_is_on:
                for led in leds:
                    led.on()
                system_is_on = True
                print("Action: LEDs ON (low light).")
                last_action_time = current_time

            elif system_is_on:
                if gesture_recognized == "Thumbs Up":
                    for led in leds:
                        led.on()
                    print("Action: All LEDs are already ON. Cannot increase brightness without PWM.")
                    last_action_time = current_time
                
                elif gesture_recognized == "Thumbs Down":
              
                    print("Action: All LEDs are flashing 2 times.")
                    for _ in range(2):
                        for led in leds:
                            led.off()
                        time.sleep(0.2)
                        for led in leds:
                            led.on()
                        time.sleep(0.2)
                    last_action_time = current_time

                elif gesture_recognized == "Left Swipe" or gesture_recognized == "Right Swipe":
                    print(f"Action: {gesture_recognized} Pattern.")
                    for pattern in get_swipe_pattern(gesture_recognized):
                        for i, state in enumerate(pattern):
                            if state:
                                leds[i].on()
                            else:
                                leds[i].off()
                        time.sleep(0.2)  
                    for led in leds:
                        led.on()
                    last_action_time = current_time

        if result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
    
    state_text = f"System: {'ON' if system_is_on else 'OFF'}"
    cv2.putText(frame, state_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.putText(frame, action_text, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('Hand Gesture Control', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()
for led in leds:
    led.off()
    led.close()
print("Program terminated.")