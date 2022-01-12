#!/bin/bash
kill -9 `ps -fA | grep gui.py | grep -v grep | awk '{print $2}'`
killall mplayer
killall -9 firefox-bin
killall xkey

