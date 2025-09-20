# FalconID (Archive)

**Originally built:** ~2024 • **Status:** Archived • **Stack:** Python (OpenCV, DJI Tello, FaceCheck API)

## What it does
**FalconID** is a prototype drone-based system that detects faces, captures images,  
and performs reverse face search through the FaceCheck API.  
Features

Face detection via OpenCV Haar Cascades.

Drone integration with DJI Tello camera (optional).

Reverse search with FaceCheck API (confidence scores + URLs).

Terminal output: match scores, URLs, thumbnails.

## Quickstart
```bash
# prerequisites
Python 3.10+
pip install -r requirements.txt

# setup
export APITOKEN=your_facecheck_api_key
# (Optional) set USE_Tello_Cam=True in facecheck.py to use DJI Tello drone camera

# run
python facecheck.py
