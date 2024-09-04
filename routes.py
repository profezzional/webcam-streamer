import cv2
from flask import Response
from app import app
from camera_streams import generate_feed, generate_snapshot

MAX_INDEX_TO_CHECK = 22

@app.route('/')
def index():
    return { 'status': 'successful' }

@app.route('/get_cameras')
def get_cameras():
    # OpenCV does not provide a direct way to list camera names, butcan check available indices
    available_cameras = {}
    
    for index in range(MAX_INDEX_TO_CHECK + 1):
        try:
            print(f'attempting to get {index}')
            cap = cv2.VideoCapture(index)
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

            if cap.read()[0]:
                available_cameras[f'Camera {index}'] = index
                print(f'got {index}')
            else:
                print(f'couldn\'t get {index}')

            cap.release()
        except:
            print(f'couldn\'t get {index}')
            continue

    return available_cameras

@app.route('/stream/<int:camera_index>', defaults= { 'frame_width': None, 'frame_height': None, 'frame_rate': None })
@app.route('/stream/<int:camera_index>/<int:frame_width>/<int:frame_height>', defaults={ 'frame_rate': None })
@app.route('/stream/<int:camera_index>/<int:frame_width>/<int:frame_height>/<int:frame_rate>')
def video_feed(camera_index, frame_width, frame_height, frame_rate):
    print(f'getting video feed for {camera_index}, {frame_width}, {frame_height}, {frame_rate}')
    return Response(generate_feed(camera_index, frame_width, frame_height, frame_rate),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stream/<int:camera_index>', defaults={ 'frame_width': None, 'frame_height': None })
@app.route('/snapshot/<int:camera_index>/<int:frame_width>/<int:frame_height>')
def snapshot(camera_index, frame_width, frame_height):
    return next(generate_snapshot(camera_index, frame_width, frame_height))
