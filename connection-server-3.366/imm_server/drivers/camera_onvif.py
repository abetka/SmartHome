#!/usr/bin/python

# camera_onvif

mjpg="http://@IP@:@HTTP_PORT@"
stream="rtsp://@USER@:@DPASSWORD@@@IP@:@RTSP_PORT@"

user="@USER@"
password="@EPASSWORD@"
passkey="@PASSKEY@"

service_port="@SERVICE_PORT@"

import Pyro.core
import sys

sys.path.append('/opt/imm/wxgui/')
import Logging
from immServerConnector import getEpsnetAddr

def controlWrapper(f):
    def wrapper(*args, **kwarg):
        move(f.__name__)
        ret = f(*args, **kwarg)
        return ret
    return wrapper

def move(cmd):
    try:
        onvif = Pyro.core.getProxyForURI("PYROLOC://%s:7770/onvif"%getEpsnetAddr())
        getattr(onvif, cmd)("@CAMERA@", "@PROFILE@")
    except Exception as e:
        Logging.error('%s: %s'%(cmd, str(e)))

@controlWrapper
def left():
    pass

@controlWrapper
def right():
    pass

@controlWrapper
def up():
    pass

@controlWrapper
def down():
    pass

@controlWrapper
def zoomIn():
    pass

@controlWrapper
def zoomOut():
    pass

