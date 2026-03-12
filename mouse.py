import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()

cap = cv2.VideoCapture(0)

frame_margin = 100
smoothening = 5
prev_x, prev_y = 0, 0
click_timer = None
dragging = False

def fingers_up(hand):
    tips = [8, 12, 16, 20]
    fingers = []
    for tip in tips:
        if hand.landmark[tip].y < hand.landmark[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

while True:
    start_time = time.time()

    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    cv2.rectangle(frame, (frame_margin, frame_margin),
                  (w - frame_margin, h - frame_margin),
                  (255, 0, 255), 2)

    status_text = "Idle"

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        finger_state = fingers_up(hand)

        index = hand.landmark[8]
        x = int(index.x * w)
        y = int(index.y * h)

        screen_x = np.interp(x, (frame_margin, w - frame_margin), (0, screen_w))
        screen_y = np.interp(y, (frame_margin, h - frame_margin), (0, screen_h))

        curr_x = prev_x + (screen_x - prev_x) / smoothening
        curr_y = prev_y + (screen_y - prev_y) / smoothening

        # MOVE MODE (Only index up)
        if finger_state == [1, 0, 0, 0]:
            pyautogui.moveTo(curr_x, curr_y)
            status_text = "Move Mode"

        # CLICK MODE (Pinch)
        thumb = hand.landmark[4]
        thumb_x = int(thumb.x * w)
        thumb_y = int(thumb.y * h)
        distance = np.hypot(x - thumb_x, y - thumb_y)

        if distance < 30:
            if click_timer is None:
                click_timer = time.time()
            elif time.time() - click_timer > 0.3:
                pyautogui.click()
                status_text = "Click"
                click_timer = None
        else:
            click_timer = None

        # SCROLL MODE (Index + Middle)
        if finger_state == [1, 1, 0, 0]:
            pyautogui.scroll(30)
            status_text = "Scroll Mode"

        # DRAG MODE (Fist)
        if finger_state == [0, 0, 0, 0]:
            if not dragging:
                pyautogui.mouseDown()
                dragging = True
            status_text = "Dragging"
        else:
            if dragging:
                pyautogui.mouseUp()
                dragging = False

        prev_x, prev_y = curr_x, curr_y

    # FPS Counter
    fps = int(1 / (time.time() - start_time))
    cv2.putText(frame, f"FPS: {fps}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.putText(frame, f"Mode: {status_text}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Advanced AI Hand Mouse", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
