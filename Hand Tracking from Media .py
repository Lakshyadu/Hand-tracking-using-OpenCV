import cv2
import mediapipe as mp
import time
from pathlib import Path

base_dir = Path(__file__).resolve().parent
video_path = str(base_dir / 'Data Sources and Artifacts' / 'input_video.mp4')
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise FileNotFoundError(f'Could not open input video: {video_path}')

# Get video details for the output video
video_fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
if video_fps <= 0 or width <= 0 or height <= 0:
    cap.release()
    raise ValueError(f'Invalid video properties: fps={video_fps}, width={width}, height={height}')

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video_path = str(base_dir / 'Data Sources and Artifacts' / 'output_video.mp4')
out = cv2.VideoWriter(output_video_path, fourcc, video_fps, (width, height))
if not out.isOpened():
    cap.release()
    raise RuntimeError(f'Could not create output video: {output_video_path}')

mphands = mp.solutions.hands
hands = mphands.Hands(False)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()

    if not success:
        break  # Break the loop if the video ends or there is an issue reading the video

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            # below code is for drawing the landmarks on the hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                if id == 0:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mphands.HAND_CONNECTIONS)

    cTime = time.time()
    display_fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(display_fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    
    # Write the frame to the output video
    out.write(img)

    # Break the loop and close the window when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video file, output video, and close the window
cap.release()
out.release()
cv2.destroyAllWindows()