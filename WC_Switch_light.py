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
import threading
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
        logging.FileHandler("WC_Switch_light.log"),
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
        return
    # tn.set_debuglevel(100)
    return tn

def telnetGet( cmd, delimeter = ';'):
    tn = telnetConnect()
    tn.write(b"GET" + delimeter.encode('ascii') + cmd.encode('ascii') + b"\r\n")
    recv = tn.read_until(b"\r\n").decode('ascii').split(';')[2].rstrip("\r").rstrip("\n")
    logging.debug("Telnet GET Answer " + cmd + ": " + recv)
    tn.close()
    return int(recv)

def telnetSet( cmd, arg, delimeter = ';'):
    tn = telnetConnect()
    tn.write(b"SET" + delimeter.encode('ascii') + cmd.encode('ascii')+ delimeter.encode('ascii')+ arg.encode('ascii') + b"\r\n")
    recv = tn.read_until(b"\r\n").decode('ascii').split(';')[2].rstrip("\r").rstrip("\n")
    logging.debug("Telnet SET Answer " + cmd + ": " + recv)
    tn.close()

def changeCurtainsState(x):
    timer = threading.Timer( 30.0, telnetSet, [x[2],'0'] )
    logging.debug("Current State for " + x[2] + " is " + x[3] )
    if int(x[3][:-5]) == 1:
            timer.start()
    logging.debug(timer.is_alive())

def changeWCSwitchState(x):
    pointLights = telnetGet("0x02030024")
    fan = telnetGet("0x02030025")
    backLightMirror = telnetGet("0x01020003")
    backLight = telnetGet("0x01020014")
    if pointLights == 0 and fan == 0:
        telnetSet("0x01020053","1")
        telnetSet("0x01020054","0")
    else:
        telnetSet("0x01020053","0")
        telnetSet("0x01020054","1")
    if backLightMirror == 0 and backLight == 0:
        telnetSet("0x01020055","1")
        telnetSet("0x01020056","0")
        telnetSet("0x0102001D","1")
        telnetSet("0x0102001E","0")
    else:
        telnetSet("0x01020055","0")
        telnetSet("0x01020056","1")
        telnetSet("0x0102001D","0")
        telnetSet("0x0102001E","1")

if __name__ == '__main__':
    try:
        tn = telnetConnect()
        while True:
            line = tn.read_until(b"\n")
            splitted_line = str(line).split(';')
            if 'EVENT' in splitted_line[0]:
                logging.debug(line)
                try:
                    switchCase = {
                        '0x02030024': changeWCSwitchState,
                        '0x02030025': changeWCSwitchState,
                        '0x01020003': changeWCSwitchState,
                        '0x01020014': changeWCSwitchState,
                        '0x01020072': changeCurtainsState,
                        '0x01020073': changeCurtainsState,
                        '0x01020074': changeCurtainsState,
                        '0x01020075': changeCurtainsState,
                        '0x0102006e': changeCurtainsState,
                        '0x0102006f': changeCurtainsState,
                        '0x01020070': changeCurtainsState,
                        '0x01020071': changeCurtainsState,
                        '0x01020076': changeCurtainsState,
                        '0x01020077': changeCurtainsState,
                        '0x01020078': changeCurtainsState,
                        '0x01020079': changeCurtainsState,
                        '0x01020026': changeCurtainsState,
                        '0x0102002f': changeCurtainsState,
                    }[splitted_line[2]](splitted_line)
                except KeyError:
                    print('')
                    # logging.debug("Key " + splitted_line[2] + " not in specific range")
    except (KeyboardInterrupt, SystemExit):
        logging.debug("The application was closed")
