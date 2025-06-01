import cv2
import mediapipe as mp

# import tensorflow as tf
import serial

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

cam = cv2.VideoCapture(0)
if not cam.isOpened():
    raise IOError("Camera cannot be opened")

# create recognizer options
model_path = "C:/Users/asava/Documents/Projects/AI-enabled-Gesture-Control-System/gesture_recognizer.task"
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1,
    min_hand_detection_confidence=0.7,
)

# create recognizer
recognizer = GestureRecognizer.create_from_options(options)

while True:
    ret, frame = cam.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    try:
        gesture = recognizer.recognize(mp_image)
        if gesture.gestures:
            top_gesture = gesture.gestures[0][0]
            gesture_name = top_gesture.category_name
            confidence = top_gesture.score

            # Display gesture on frame
            cv2.putText(
                frame,
                f"Gesture: {gesture_name}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
            cv2.putText(
                frame,
                f"Confidence: {confidence:.2f}",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            # Print to console
            print(f"Detected: {gesture_name} (Confidence: {confidence:.2f})")

            if gesture_name == "Unknown" and confidence > 0.7:
                arduino_num = 0
            elif gesture_name == "Closed_fist" and confidence > 0.7:
                arduino_num = 1
            elif gesture_name == "Open_Palm" and confidence > 0.7:
                arduino_num = 2

            # draw points
            if gesture.hand_landmarks:
                for hand_landmarks in gesture.hand_landmarks:
                    # Draw landmarks on frame
                    for landmark in hand_landmarks:
                        x = int(landmark.x * frame.shape[1])
                        y = int(landmark.y * frame.shape[0])
                        cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)

        else:
            cv2.putText(
                frame,
                "No gesture detected",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )

    except Exception as e:
        print(f"Error in gesture recognition: {e}")
        cv2.putText(
            frame,
            "Recognition Error",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
