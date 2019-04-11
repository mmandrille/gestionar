#!/bin/bash
cd /opt/gestionar
source venv/bin/activate
cd /opt/gestionar/gestionar
python manage.py process_tasks
