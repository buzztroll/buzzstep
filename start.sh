#!/usr/bin/env bash

cd /home/bresnaha/Dev/buzzstep
. /home/bresnaha/Dev/buzzstep/venv/bin/activate
touch step.log
python monitor.py db.sqlite3 > step.log
