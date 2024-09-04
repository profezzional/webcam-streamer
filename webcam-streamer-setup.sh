# create python env     webcam-streamer-env
# activate env
# install requirements
# create service file (inject current directory to working co)
# sudo systemctl daemon-reload
# enable and start service
# check status
# if status is good, exit, otherwise report error


# [Unit]
# Description=Webcam Streamer Flask Server

# [Service]
# ExecStart=python app.py
# WorkingDirectory=/home/pi/webcam-streamer
# Environment="PATH=/home/pi/webcam-streamer/webcam-streamer-env/bin"
# User=pi
# Group=pi
# Restart=always

# [Install]
# WantedBy=multi-user.target
