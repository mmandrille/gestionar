#!/bin/bash
cd /opt/gestionar
source venv/bin/activate
cd /opt/gestionar/gestionar
gunicorn gestionar.wsgi -t 600 -b 127.0.0.1:8012 -w 6 --user=servidor --group=servidor --log-file=/opt/gestionar/gunicorn.log 2>>/opt/gestionar/gunicorn.log

