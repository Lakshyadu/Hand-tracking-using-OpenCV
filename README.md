# Hand Tracking using OpenCV & MediaPipe

<p align="center">
  <img src="assets/infographic.png" alt="Hand tracking infographic: features, how it works, project structure, the 21 hand landmarks, how to run, detector settings and quick fixes" width="100%">
</p>

Real-time hand tracking in Python. The project uses **OpenCV** for video capture and display, and **MediaPipe Hands** to detect hands and locate their 21 landmarks in every frame.

It includes two scripts:

| Script | Input | What it does |
|--------|-------|--------------|
| `app.py` | Live webcam | Tracks hands in real time and shows an FPS counter |
| `Hand_Tracking_from_Media.py` | Video file (`input_video.mp4`) | Tracks hands in a recorded video and saves the annotated result as `output_video.mp4` |

---

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [How It Works](#how-it-works)
- [Hand Landmarks](#hand-landmarks)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Code Walkthrough](#code-walkthrough)
- [Configuration and Customization](#configuration-and-customization)
- [Troubleshooting](#troubleshooting)
- [Applications and Ideas](#applications-and-ideas)
- [License](#license)

---

## Features

- Real-time hand detection and tracking from a webcam
- Detects and tracks hands in pre-recorded video and saves an annotated copy
- Draws all 21 landmarks per hand and the connections between them
- Highlights the wrist (landmark 0) with a filled magenta circle
- Prints every landmark's pixel coordinates (`id x y`) to the console
- On-screen FPS counter in the top-left corner
- Input checks in the video script (missing file, invalid video properties, output writer failure) with clear error messages
- Press `q` to quit at any time
- Minimal dependencies: only `opencv-python` and `mediapipe`

---

## Demo

Add your screenshots or GIFs here. For example:

```markdown
![Webcam demo](assets/webcam_demo.png)
```

A sample output video from the video-processing script can be placed in `Data Sources and Artifacts/` (it is saved there as `output_video.mp4`).

---

## How It Works

```
 Webcam / video file
        │
        ▼
 OpenCV reads a frame (BGR)
        │
        ▼
 Convert BGR → RGB
        │
        ▼
 MediaPipe Hands  ──►  21 landmarks per detected hand (normalized x, y, z)
        │
        ▼
 Convert normalized coordinates → pixel coordinates (x * width, y * height)
        │
        ▼
 Draw landmarks + connections + FPS with OpenCV
        │
        ▼
 Display in a window  (video script also writes the frame to output_video.mp4)
```

MediaPipe uses a two-stage pipeline. A palm detector first finds hands in the image, then a hand landmark model predicts the 21 key points on each hand. When tracking mode is on (`static_image_mode=False`, as used here), the detector only re-runs when needed, which keeps the frame rate high.

---

## Hand Landmarks

MediaPipe returns 21 landmarks per hand, indexed 0 to 20:

| ID | Landmark | ID | Landmark |
|----|----------|----|----------|
| 0 | Wrist | 11 | Middle finger PIP |
| 1 | Thumb CMC | 12 | Middle finger tip |
| 2 | Thumb MCP | 13 | Ring finger MCP |
| 3 | Thumb IP | 14 | Ring finger PIP |
| 4 | Thumb tip | 15 | Ring finger DIP |
| 5 | Index finger MCP | 16 | Ring finger tip |
| 6 | Index finger PIP | 17 | Pinky MCP |
| 7 | Index finger DIP | 18 | Pinky PIP |
| 8 | Index finger tip | 19 | Pinky DIP |
| 9 | Middle finger MCP | 20 | Pinky tip |
| 10 | Middle finger DIP | | |

Each landmark has normalized `x` and `y` values (0.0 to 1.0, relative to the frame) and a relative depth `z`. The scripts convert `x` and `y` to pixels using the frame width and height.

---

## Project Structure

```
.
├── app.py                          # Real-time webcam hand tracking
├── Hand_Tracking_from_Media.py     # Hand tracking on a video file, saves output
├── assets/
│   └── infographic.png             # Infographic shown at the top of this README
├── Data Sources and Artifacts/
│   ├── input_video.mp4             # Input video for the video script
│   └── output_video.mp4            # Generated annotated video
├── requirements.txt                # Python dependencies
├── .gitignore
├── LICENSE                         # GNU GPL v3
└── README.md
```

---

## Requirements

- Python 3.8 to 3.12 (use a version supported by your installed `mediapipe` release)
- A webcam (for `app.py` only)
- Packages listed in `requirements.txt`:
  - `opencv-python`
  - `mediapipe`

---

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Lakshyadu/Hand-tracking-using-OpenCV.git
   cd Hand-tracking-using-OpenCV
   ```

2. **Create a virtual environment** (recommended)

   ```bash
   python -m venv .venv

   # Linux / macOS
   source .venv/bin/activate

   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### 1. Live webcam tracking

```bash
python app.py
```

- A window titled **Image** opens with your webcam feed.
- Show your hand to the camera. Landmarks and connections are drawn on it.
- The wrist is marked with a magenta circle, and the FPS appears at the top-left.
- Landmark coordinates are printed in the terminal as `id x y`.
- Press **`q`** to quit.

### 2. Tracking on a video file

1. Put your video at `Data Sources and Artifacts/input_video.mp4`.
2. Run:

   ```bash
   python Hand_Tracking_from_Media.py
   ```

3. A preview window shows the annotated frames while processing.
4. The result is saved to `Data Sources and Artifacts/output_video.mp4`.
5. Press **`q`** to stop early. The frames processed so far are still saved.

The output has the same resolution and frame rate as the input.

---

## Code Walkthrough

### `app.py` (webcam)

1. **Setup**: opens the default camera with `cv2.VideoCapture(0)` and creates the MediaPipe `Hands` object and drawing utilities.
2. **Frame loop**: reads a frame, converts it from BGR to RGB (MediaPipe expects RGB), and runs `hands.process()`.
3. **Landmark handling**: for each detected hand, loops through the 21 landmarks and converts normalized coordinates to pixels:
   ```python
   cx, cy = int(lm.x * w), int(lm.y * h)
   ```
   It prints each point and draws a filled circle on landmark 0.
4. **Drawing**: `mpDraw.draw_landmarks(...)` draws the skeleton using `HAND_CONNECTIONS`.
5. **FPS**: computed from the time between frames (`1 / (cTime - pTime)`) and drawn with `cv2.putText`.
6. **Exit**: pressing `q` breaks the loop, then the camera is released and windows are closed.

### `Hand_Tracking_from_Media.py` (video file)

Same detection logic as above, plus:

- **Path handling** with `pathlib`, so the script finds `Data Sources and Artifacts/` relative to its own location regardless of where you run it from.
- **Validation**: raises `FileNotFoundError` if the input video cannot be opened, `ValueError` if the video reports invalid fps or size, and `RuntimeError` if the output writer cannot be created.
- **Output writer**: `cv2.VideoWriter` with the `mp4v` codec, using the input video's fps and resolution.
- **Clean ending**: the loop stops when the video ends (`success` is `False`) or when `q` is pressed, then both the reader and writer are released.

---

## Configuration and Customization

The scripts use `mphands.Hands(False)`, which sets `static_image_mode=False` and leaves everything else at the defaults. You can pass more options:

```python
hands = mphands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)
```

| Parameter | Effect |
|-----------|--------|
| `static_image_mode` | `False` tracks across frames (faster). `True` runs detection on every frame |
| `max_num_hands` | Maximum number of hands to detect |
| `min_detection_confidence` | Raise it to reduce false detections |
| `min_tracking_confidence` | Raise it for stricter tracking, lower it for smoother tracking |

Other easy changes:

- **Different camera**: change `cv2.VideoCapture(0)` to `1`, `2`, and so on.
- **Highlight another landmark**: change `if id == 0:` (for example `4` for the thumb tip or `8` for the index fingertip).
- **Quieter console**: remove the `print(id, cx, cy)` line.
- **Different video**: change the filename in `video_path`.

---

## Troubleshooting

| Problem | Possible fix |
|---------|--------------|
| `FileNotFoundError: Could not open input video` | Check that `Data Sources and Artifacts/input_video.mp4` exists and the folder name matches exactly |
| Webcam window is black or the script crashes immediately | Make sure no other app is using the camera, or try camera index `1` |
| `AttributeError: module 'mediapipe' has no attribute 'solutions'` | Your installed MediaPipe version may not include the legacy `solutions` API. Install an older release, for example `pip install "mediapipe<0.10.20"` (adjust if needed) |
| `pip install mediapipe` fails | Your Python version may be unsupported. Use Python 3.8 to 3.12 |
| Low FPS | Lower the camera or video resolution, close other apps, or keep `static_image_mode=False` |
| Output video will not play | Try a different player or change the codec in `cv2.VideoWriter_fourcc` |
| Hands are not detected | Improve lighting, keep the hand fully in frame, and avoid cluttered backgrounds |
| Window will not close | Click on the video window first, then press `q` |

---

## Applications and Ideas

Hand landmarks are a starting point for many projects:

- Gesture-based volume or brightness control (distance between thumb tip and index tip)
- Finger counting
- Virtual mouse or air-drawing
- Sign language recognition
- Touchless interfaces and presentations
- Games and AR/VR interaction

Planned improvements:

- Left/right hand labels
- Finger up/down detection
- Gesture recognition
- Refactor the tracking logic into a reusable `HandTracker` class
- Command-line arguments for input and output paths

---

## License

This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- [OpenCV](https://opencv.org/) for computer vision and video I/O
- [MediaPipe](https://developers.google.com/mediapipe) by Google for the hand tracking models
