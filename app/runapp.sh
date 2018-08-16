#!/bin/sh
gunicorn -w 1 -b 0.0.0.0:$PORT --timeout 1000 app:app
