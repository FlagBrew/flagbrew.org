#!/bin/bash

/usr/bin/screen -dmS flagbrew.org /usr/bin/gunicorn -w 1 --reload -b 0.0.0.0:4000 app:app