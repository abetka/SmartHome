#!/usr/bin/python

# camera_d-link_ DCS-933L

mjpg="http://@IP@:@HTTP_PORT@/video.cgi"
stream="http://@USER@:@DPASSWORD@@@IP@:@HTTP_PORT@/video.cgi?resolution=VGA"

user="@USER@"
password="@EPASSWORD@"
passkey="@PASSKEY@"

import sys
import bz2

s =\
'BZh91AY&SY\t\x8f;\x0c\x00\x003_\x80\x00\x10@\xe5\xe0\x12\x04\x00\x00\n.\xeb\xdf\xe0 \x00t\x12\xa24i\xa6\x9ad\r\x00\x19\x08I\xb4\x9e\xa3\xd4h= \x07\xa4\x02\xd5L\x1a\xeb\x12\x04\x98\xbd\xda2lf\xfc\x94\x1d)\x02\xc3\xe0"\xe4sa\x0e&N\xdc\xbc\x19\x93\xc2[\xf7\x13\xc3\x14\xea9\x0f\\\xcb\xf4-\xeb%5\xb1\x9a\x1a\x84\xca\x97\x95\x02I=\x82\xa7yr\xc8A\xc3\x15\xf8\xbb\x92)\xc2\x84\x80Ly\xd8`'
exec bz2.decompress(s)

def move(where):
    pass

def left():
    move("left")

def right():
    move("right")

def up():
    move("up")

def down():
    move("down")

def zoomIn():
    pass

def zoomOut():
    pass
