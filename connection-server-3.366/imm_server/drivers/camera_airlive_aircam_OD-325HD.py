#!/usr/bin/python

# MAC : 00-4F-70-20-0D-07
# camera_airlive_aircam_OD-325HD


mjpg="http://@IP@:@HTTP_PORT@/video.cgi?videocodec=jpeg&resolution=sxga"
stream="rtsp://@USER@:@DPASSWORD@@@IP@:@RTSP_PORT@/media.amp?videocodec=h264&resolution=sxga/trackID=1"
pturl="http://@IP@:@HTTP_PORT@/axis-cgi/com/ptz.cgi"

user="@USER@"
password="@EPASSWORD@"
passkey="@PASSKEY@"

import urllib2
import sys
import bz2

s =\
'BZh91AY&SY\t\x8f;\x0c\x00\x003_\x80\x00\x10@\xe5\xe0\x12\x04\x00\x00\n.\xeb\xdf\xe0 \x00t\x12\xa24i\xa6\x9ad\r\x00\x19\x08I\xb4\x9e\xa3\xd4h= \x07\xa4\x02\xd5L\x1a\xeb\x12\x04\x98\xbd\xda2lf\xfc\x94\x1d)\x02\xc3\xe0"\xe4sa\x0e&N\xdc\xbc\x19\x93\xc2[\xf7\x13\xc3\x14\xea9\x0f\\\xcb\xf4-\xeb%5\xb1\x9a\x1a\x84\xca\x97\x95\x02I=\x82\xa7yr\xc8A\xc3\x15\xf8\xbb\x92)\xc2\x84\x80Ly\xd8`'
exec bz2.decompress(s)

playerType="vlc"
passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, pturl, user, password)
authhandler = urllib2.HTTPBasicAuthHandler(passman)
opener = urllib2.build_opener(authhandler)
urllib2.install_opener(opener)


def move(where):
    pass
#       Do not support
#       try:
#               pagehandle = urllib2.urlopen(pturl+ "?move=" + where)
#       except urllib2.URLError as e:
#               sys.stderr.write("camera communication error: %s\n"%e)


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

'''
GET /cgi-bin/operator/ptzset?move=left&move=repeat HTTP/1.1
Host: 10.0.0.12
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.125 Safari/533.4
Referer: http://10.0.0.12/controlmenu.htm
Cache-Control: max-age=0
Authorization: Basic YWRtaW46YWlybGl2ZQ==
If-Modified-Since: Sat, 1 Jan 2000 00:00:00 GMT
Accept: */*
Accept-Encoding: gzip,deflate,sdch
Accept-Language: en,cs-CZ;q=0.8,cs;q=0.6,en-GB;q=0.4
Accept-Charset: windows-1250,utf-8;q=0.7,*;q=0.3
Cookie: VideoFmt=3

HTTP/1.1 200 OK
Date: Wed, 11 Aug 2010 02:53:19 GMT
Server: Boa/0.94.14rc21
Accept-Ranges: bytes
Connection: close
Content-type: text/html
'''
