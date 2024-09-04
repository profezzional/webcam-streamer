import signal
import sys
from flask import Flask
import time

app = Flask(__name__)
from routes import * # need to import routes after flask server is created, or everything is a 404

HOST = '0.0.0.0'
PORT = 8081
RESTART_TIME_SEC = 5

def signal_handler(signal, frame):
    print('Received SIGINT (Ctrl+C), shutting down gracefully...')
    sys.exit(0)

def run_server():
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            print('Starting Flask server...')
            app.run(host = HOST, port = PORT)
        except Exception as e:
            print(f'Error: {e}. Restarting server in {RESTART_TIME_SEC} seconds...')
            time.sleep(RESTART_TIME_SEC)
            
            continue

if __name__ == '__main__':
    run_server()