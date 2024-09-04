from flask import Response
from camera_stream import CameraStream

camera_streams = {}

def generate_feed(camera_index, frame_width=None, frame_height=None, fps=None):
    if camera_index not in camera_streams:
        camera_stream = CameraStream(camera_index, frame_width, frame_height, fps)

        if not camera_stream.start():
            print(f'Error: Failed to start camera stream {camera_index}')
            return
        
        camera_streams[camera_index] = camera_stream

    if not camera_streams[camera_index].running:
        print(f'Error: Camera stream {camera_index} is not running')

        return

    while True:
        if camera_index not in camera_streams:
            print(f'camera index not in streams')
            break

        frame = camera_streams[camera_index].get_frame()

        if frame is None:
            print(f'frame is none')
            break

        yield frame

def generate_snapshot(camera_index, frame_width=None, frame_height=None):
    if camera_index not in camera_streams:
        camera_streams[camera_index] = CameraStream(camera_index, frame_width, frame_height)

    frame = camera_streams[camera_index].get_frame()

    if frame is None:
        yield Response('Error: could not capture frame')
    else:
        yield Response(frame, mimetype='image/jpeg')