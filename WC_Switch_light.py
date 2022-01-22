import sys
import telnetlib
from datetime import datetime
from datetime import date
from datetime import timedelta
import time
import os
from apscheduler.schedulers.background import BackgroundScheduler
from astral.sun import sun
from astral import LocationInfo
import logging
#--configuration
tn_ip = "192.168.88.246"
tn_port = "1111"
city = "Kiev"
country = "Ukraine"
timezone = "Europe/London"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("sunset-sunrise-debug.log"),
        logging.StreamHandler()
    ]
)

close_curtains = ["0x01020072", "0x0102006F", "0x01020077","0x01020026"]
open_curtains = ["0x01020073", "0x0102006E", "0x01020076","0x0102002F"]

# telnetSet("0x01020029","0")
# zakrit_shtory_spalnya 0x01020072 0x00000000
# otkrit_shtory_spalnya 0x01020073
# 0x01020029
# otkrit_shtory_detskaya 0x0102006E 0x00000000
# zakrit_shtory_detskaya 0x0102006F 0x00000000
# otkrit_shtory_kuhnya 0x01020076 0x00000000
# zakrit_shtory_kuhnya 0x01020077 0x00000000
# zakrit_shtory_kabinet 0x01020026 0x00000000
# otkrit_shtory_kabinet 0x0102002F 0x00000000
#========
def telnetConnect(host = tn_ip,port = tn_port):
    try:
        tn = telnetlib.Telnet(tn_ip, tn_port, 15)
    except:
        logging.debug("Unable to connect to Telnet server: " + tn_ip)
        # print("Unable to connect to Telnet server: " + tn_ip)
        return
    # tn.set_debuglevel(100)
    return tn

def telnetGet( cmd, delimeter = ';'):
    tn = telnetConnect()
    tn.write(b"GET" + delimeter.encode('ascii') + cmd.encode('ascii') + b"\r\n")
    recv = tn.read_until(b"\r\n").decode('ascii').split(';')[2].rstrip("\r").rstrip("\n")
    logging.debug("Telnet GET Answer " + cmd + ": " + recv)
    return recv
    tn.close()

def telnetSet( cmd, arg, delimeter = ';'):
    tn = telnetConnect()
    tn.write(b"SET" + delimeter.encode('ascii') + cmd.encode('ascii')+ delimeter.encode('ascii')+ arg.encode('ascii') + b"\r\n")
    recv = tn.read_until(b"\r\n").decode('ascii').split(';')[2].rstrip("\r").rstrip("\n")
    logging.debug("Telnet SET Answer " + cmd + ": " + recv)
    tn.close()

if __name__ == '__main__':
    pointLights = telnetGet("0x0102002E")
    fan = telnetGet("0x01020025")
    backLightMirror = telnetGet("0x01020003")
    backLight = telnetGet("0x01020014")
    if int(pointLights) == 0 and int(fan) == 0 :
        telnetSet("0x01020053","1")
        telnetSet("0x01020054","0")
    else:
        telnetSet("0x01020053","0")
        telnetSet("0x01020054","1")
    if int(backLightMirror) == 0 and int(backLight) == 0 :
        telnetSet("0x01020055","1")
        telnetSet("0x01020056","0")
    else:
        telnetSet("0x01020055","0")
        telnetSet("0x01020056","1")