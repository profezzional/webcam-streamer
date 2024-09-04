import cv2
from threading import Thread, Lock
import time

MAX_CONCURRENT_ERRORS = 20
DEFAULT_FPS = 30
DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 480
HIGH_VALUE = 100000

class CameraStream:
    def __init__(self, camera_index, frame_width = DEFAULT_WIDTH, frame_height = DEFAULT_HEIGHT, frame_rate = DEFAULT_FPS):
        self.camera_index = camera_index
        self.lock = Lock()
        self.frame = None
        self.last_frame_successful = True
        self.running = False
        self.thread = None
        self.concurrent_errors = 0

        self.videoCapture = cv2.VideoCapture(self.camera_index)
        self.videoCapture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

        if not self.videoCapture.isOpened():
            print(f'Error: Failed to open camera stream {self.camera_index}')

            return self.on_init_failed()
        
        self.videoCapture.set(cv2.CAP_PROP_FPS, frame_rate or DEFAULT_FPS)
        self.videoCapture.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width or DEFAULT_WIDTH)
        self.videoCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height or DEFAULT_HEIGHT)

        self.frame_rate = frame_rate or DEFAULT_FPS
        self.frame_width = frame_width or DEFAULT_WIDTH
        self.frame_height = frame_height or DEFAULT_HEIGHT

    def on_init_failed(self):
        self.videoCapture = None
        
    def start(self):
        if self.running:
            return
        
        if self.videoCapture is None:
            print(f'Error: Cannot start camera stream {self.camera_index}')
            return False
        
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.running = True # this has to be set before the thread starts
        self.thread.start()

        return True

    def stop(self):
        if not self.running:
            return
        
        self.running = False

        if self.thread:
            self.thread.join()

        if self.videoCapture:
            self.videoCapture.release()

        self.videoCapture = None
        self.thread = None

    def update(self):
        while self.running:
            with self.lock:
                self.last_frame_successful, frame = self.videoCapture.read()

                if not self.last_frame_successful:
                    self.concurrent_errors += 1
                    print(f'Warning: failed to grab frame from camera {self.camera_index}')
                    time.sleep(0.1)

                    if self.concurrent_errors == MAX_CONCURRENT_ERRORS:
                        print(f'Max concurrent frame errors reached; stopping stream {self.camera_index}')
                        self.stop()

                        break

                    continue
                else:
                    self.concurrent_errors = 0

                self.frame = cv2.resize(frame, (self.frame_width, self.frame_height))

            time.sleep(1.0 / self.frame_rate)

    def get_frame(self):
        with self.lock:
            if self.last_frame_successful and self.frame is not None:
                _, buffer = cv2.imencode('.jpg', self.frame)
                
                return (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            else:
                return None

    def __del__(self):
        self.stop()