import cv2
import mediapipe
import pyautogui
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class HandGestureDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hand Gesture Detection")
        
        # Video capture variables
        self.camera = cv2.VideoCapture(0)
        self.capture_hands = mediapipe.solutions.hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
        self.display_width = 640
        self.display_height = 480
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Cursor access control variables
        self.cursor_access = False
        self.cursor_control_active = False
        
        # Welcome message label
        self.welcome_label = tk.Label(root, text="Welcome to Hand Gesture Control System!")
        self.welcome_label.pack()
        
        # Video label
        self.video_label = tk.Label(root)
        self.video_label.pack()
        
        # Start button
        self.start_button = tk.Button(root, text="Start", command=self.start_detection)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Stop button
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_detection)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Variables for tracking index finger position
        self.prev_index_tip_y = 0
        self.index_forward_count = 0

    def start_detection(self):
        self.cursor_access = True
        self.cursor_control_active = True
        self.detect_hand_gesture()
    
    def stop_detection(self):
        self.cursor_access = False
        self.cursor_control_active = False
    
    def detect_hand_gesture(self):
        ret, image = self.camera.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture video frame.")
            return
        
        image = cv2.flip(image, 1)
        resized_image = cv2.resize(image, (self.display_width, self.display_height))
        rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        output_hands = self.capture_hands.process(rgb_image)
        all_hands = output_hands.multi_hand_landmarks
        
        if all_hands:
            for hand in all_hands:
                mediapipe.solutions.drawing_utils.draw_landmarks(
                    resized_image, hand, mediapipe.solutions.hands.HAND_CONNECTIONS)
                
                fingers_up = [hand.landmark[4].y < hand.landmark[3].y,  # Thumb
                              hand.landmark[8].y < hand.landmark[7].y,  # Index finger
                              hand.landmark[12].y < hand.landmark[11].y,  # Middle finger
                              hand.landmark[16].y < hand.landmark[15].y,  # Ring finger
                              hand.landmark[20].y < hand.landmark[19].y]  # Pinky finger

                # Click gesture: Index finger up and all other fingers down
                if fingers_up[1] and all(not finger_up for i, finger_up in enumerate(fingers_up) if i != 1):
                    pyautogui.click()

                # Copy gesture: Middle finger up and all other fingers down
                if fingers_up[2] and all(not finger_up for i, finger_up in enumerate(fingers_up) if i != 2):
                    pyautogui.hotkey('ctrl', 'c')

                # Select gesture: Ring finger up and all other fingers down
                if fingers_up[3] and all(not finger_up for i, finger_up in enumerate(fingers_up) if i != 3):
                    pyautogui.hotkey('ctrl', 'a')

                # Scroll gesture: Thumb and Pinky finger up and all other fingers down
                if all(fingers_up[i] for i in [0, 4]) and all(not fingers_up[i] for i in [1, 2, 3]):
                    pyautogui.scroll(10)
                
                # Volume increase gesture: Thumb and Index finger up, Middle, Ring, and Pinky fingers down
                if all(fingers_up[i] for i in [0, 1]) and all(not fingers_up[i] for i in [2, 3, 4]):
                    pyautogui.hotkey('volumeup')

                # Volume decrease gesture: Thumb and Middle finger up, Index, Ring, and Pinky fingers down
                if all(fingers_up[i] for i in [0, 2]) and all(not fingers_up[i] for i in [1, 3, 4]):
                    pyautogui.hotkey('volumedown')
                
                # Move cursor if cursor control is active
                if self.cursor_access and self.cursor_control_active:
                    x = int(hand.landmark[8].x * self.display_width)
                    y = int(hand.landmark[8].y * self.display_height)
                    mouse_x = int(pyautogui.size()[0] / self.display_width * x)
                    mouse_y = int(pyautogui.size()[1] / self.display_height * y)
                    pyautogui.moveTo(mouse_x, mouse_y)
                    
                # Check if the index finger moved forward twice
                index_tip_y = hand.landmark[8].y
                if index_tip_y < self.prev_index_tip_y:
                    self.index_forward_count += 1
                    if self.index_forward_count == 2:
                        pyautogui.click()
                else:
                    self.index_forward_count = 0

                # Update previous index finger position
                self.prev_index_tip_y = index_tip_y
        
        if self.cursor_control_active:
            self.video_label.imgtk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)))
            self.video_label.config(image=self.video_label.imgtk)
            self.video_label.after(10, self.detect_hand_gesture)
        else:
            messagebox.showinfo("Info", "Hand gesture detection stopped.")
        
    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.camera.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = HandGestureDetectionApp(root)
    root.mainloop()