#!/bin/bash

export GEVENT_MONITOR_THREAD_ENABLE=1

gunicorn -w 2 -k gevent -b 0.0.0.0:5555 main:app
