# Virtual_Mouse
This project implements a Virtual Mouse using Computer Vision that allows users to control the system cursor with hand gestures captured through a webcam.
It uses MediaPipe hand tracking and OpenCV to detect hand landmarks and perform mouse actions like move, click, scroll, and drag.

## Features

    🖱️ Move cursor using index finger
    
    👌 Pinch gesture for mouse click
    
    ✌️ Index + Middle finger for scrolling
    
    ✊ Closed fist for drag operation
    
    📷 Real-time hand tracking using webcam
    
    ⚡ Smooth cursor movement using interpolation
    
  ## 📚 Required Libraries

This project requires the following Python libraries:

- **OpenCV (cv2)** – Used for webcam capture and image processing.
- **MediaPipe** – Provides real-time hand tracking and hand landmark detection.
- **PyAutoGUI** – Used to control mouse movements, clicks, scrolling, and dragging.
- **NumPy** – Helps in numerical operations and coordinate mapping.
- **Time** – Used for FPS calculation and gesture timing.

Install the required libraries using:

```bash
pip install opencv-python mediapipe pyautogui numpy
```

## 🧪 Virtual Environment (Recommended)

Create a virtual environment for better dependency management:

```bash
python -m venv venv
```

---

## ▶️ Run the Project

```bash
python main.py
```

Make sure your system has a **working webcam**, as the project uses real-time hand tracking to control the mouse.

