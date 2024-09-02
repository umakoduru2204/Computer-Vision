# COMPUTER-VISION
# Hand Gesture Control System 

This project is a Python-based application designed to provide a hands-free control interface for your computer using real-time hand gesture recognition. Utilizing a webcam, this system detects hand gestures and translates them into various actions such as mouse clicks, copying, selecting, scrolling, and adjusting volume. This innovative solution offers an intuitive way for users to interact with their devices, particularly beneficial for individuals with limited mobility or those seeking alternative input methods.

## Features
Real-time Hand Gesture Detection: Uses the MediaPipe library to track hand movements and recognize gestures.
Action Control: Supports various actions like clicking, copying, selecting, scrolling, and volume control based on detected hand gestures.
Cursor Movement: Allows users to move the cursor on the screen by moving their hands.
User Interface: Provides a simple graphical interface with start and stop buttons for controlling hand gesture detection.

## Requirements
Python 3.x
OpenCV
MediaPipe
PyAutoGUI
Tkinter
PIL

## Installation
Install the dependencies:
pip install opencv-python mediapipe pyautogui pillow

Run the application:
python Mouse_Control.py

## Usage
Launch the application.
Click the "Start" button to begin hand gesture detection.
Perform hand gestures in front of the webcam to control actions:
Click: Raise the index finger with other fingers down.
Select: Raise the ring finger with other fingers down.
Scroll: Raise the thumb and pinky finger with other fingers down.
Volume Increase: Raise the thumb and index finger with other fingers down.
Volume Decrease: Raise the thumb and middle finger with other fingers down.
Click the "Stop" button to stop hand gesture detection.
Close the application window to exit.

## Notes
Ensure your webcam is properly configured and accessible by OpenCV.
Adjust the detection confidence and other parameters in the code as needed for optimal performance.
The application is tested on Windows but should work on other platforms with minor adjustments.
