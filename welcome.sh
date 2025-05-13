#!/usr/bin/env bash

#mpg123 /home/bresnaha/grinch.mp3 &
#mpg123 /home/bresnaha/scary-welcome.mp3 &> /dev/null
#sudo  /home/bresnaha/Dev/cottage/.venv/bin/buzz-welcome-lights &

. /home/bresnaha/Dev/cottage/.venv/bin/activate
/home/bresnaha/Dev/SLACK/slack-photo-uploader/send-snap.sh &
#sudo -E /home/bresnaha/Dev/cottage/.venv/bin/python /home/bresnaha/Dev/buzzstep/lights1.py &
sleep 60
wait
