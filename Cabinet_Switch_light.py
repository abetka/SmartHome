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

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("WC_Switch_light.log"),
        logging.StreamHandler()
    ]
)

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
    try:
        return int(recv)
    except ValueError:
        return 0

def telnetSet( cmd, arg, delimeter = ';'):
    tn = telnetConnect()
    tn.write(b"SET" + delimeter.encode('ascii') + cmd.encode('ascii')+ delimeter.encode('ascii')+ arg.encode('ascii') + b"\r\n")
    recv = tn.read_until(b"\r\n").decode('ascii').split(';')[2].rstrip("\r").rstrip("\n")
    logging.debug("Telnet SET Answer " + cmd + ": " + recv)
    tn.close()

def changeSwitchState():
    pointLights = telnetGet("0x0102002e")
    fan = telnetGet("0x01020025")
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
    else:
        telnetSet("0x01020055","0")
        telnetSet("0x01020056","1")
    if backLightMirror == 0 and backLight == 0 and fan == 0:
        telnetSet("0x0102001D","1")
        telnetSet("0x0102001E","0")
    else:
        telnetSet("0x0102001D","0")
        telnetSet("0x0102001E","1")
def manageRoom(x):
    logging.debug("managedWCSwitch ")
    print(x)
    pointLights = telnetGet("0x0102002e")
    fan = telnetGet("0x01020025")
    backLights = telnetGet("0x01020014")
    mirrorLights = telnetGet("0x01020003")
    fanSwitch = ['0x01010048', '0x0101001a']
    lightSwitch = ['0x01010049', '0x01010019']
    # Up1
    if int(x[1]) == 29 and x[2] == '0x01010047' and int(x[3][:-5]) == 1:
        if pointLights == 0:
            telnetSet("0x0102002e","1")
        else:
            telnetSet("0x0102002e","0")
        if fan == 0 and pointLights == 0:
            telnetSet('0x01020025','1')
    # Down1 Down1 inside
    if int(x[1]) == 29 and x[2] in fanSwitch and int(x[3][:-5]) == 1:
        if fan == 0:
            telnetSet('0x01020025','1')
        else:
            telnetSet('0x01020025','0')
    # Up2 Up1 inside
    if int(x[1]) == 29 and x[2] in lightSwitch and int(x[3][:-5]) == 1:
        if backLights == 0:
            telnetSet("0x01020014","1")
        else:
            telnetSet("0x01020014","0")
        if mirrorLights == 0:
            telnetSet("0x01020003","1")
        else:
            telnetSet("0x01020003","0")
    # Down2
    if int(x[1]) == 29 and x[2] == '0x0101004a' and int(x[3][:-5]) == 1:
        telnetSet("0x01020003","0")
        telnetSet("0x01020014","0")
        telnetSet("0x0102002e","0")
        telnetSet('0x01020025','0')
    # WaterLeak
    if int(x[1]) == 29 and x[2] == '0x0101000a' and int(x[3][:-5]) == 1:
        telnetSet('0x01020027','1')
    if int(x[1]) == 30 and x[2] == '0x0101000a' and int(x[3][:-5]) == 0:
        telnetSet('0x01020027','0')

if __name__ == '__main__':
    try:
        tn = telnetConnect()
        SwitchState = [
            '0x0102002e',
            '0x01020025',
            '0x01020003',
            '0x01020014',
        ]
        Switch = [
            '0x01010039',
            '0x0101003a',
            '0x0101003b',
            '0x0101003c',
            '0x0101003d',
            '0x0101003e',
            '0x0101000a',

Cabinet_Switch_Up1 GSB3-60_Up1_024E65 0x01010039 0x00000000
Cabinet_Switch_Down1 GSB3-60_Down1_024E65 0x0101003A 0x00000000
Cabinet_Switch_Up2 GSB3-60_Up2_024E65 0x0101003B 0x00000000
Cabinet_Switch_Down2 GSB3-60_Down2_024E65 0x0101003C 0x00000000
Cabinet_Switch_Up3 GSB3-60_Up3_024E65 0x0101003D 0x00000000
Cabinet_Switch_Down3 GSB3-60_Down3_024E65 0x0101003E 0x00000000
Cabinet_Switch_Green1 GSB3-60_Green1_024E65 0x01020048 0x00000000
Cabinet_Switch_Red1 GSB3-60_Red1_024E65 0x01020049 0x00000000
Cabinet_Switch_Green2 GSB3-60_Green2_024E65 0x0102004A 0x00000000
Cabinet_Switch_Red2 GSB3-60_Red2_024E65 0x0102004B 0x00000000
Cabinet_Switch_Green3 GSB3-60_Green3_024E65 0x0102004C 0x00000000
Cabinet_Switch_Red3 GSB3-60_Red3_024E65 0x0102004D 0x00000000
Cabinet_Switch_Therm_Inter GSB3-60_Inter-Therm_024E65 0x01050017 0x00000000 °C
Cabinet_Switch_Therm GSB3-60_AIN1-AIN2-Therm_024E65 0x01050018 0x00000000 °C
Cabinet_Switch_DIN1 GSB3-60_DIN1_024E65 0x0101003F 0x00000000
Cabinet_Switch_DIN2 GSB3-60_DIN2_024E65 0x01010040 0x00000000
Cabinet_Switch_Light_In GSB3-60_Light-IN_024E65 0x0102004E 0x00000000


        ]
        while True:
            try:
                line = tn.read_until(b"\n")
                logging.debug("Used Current Telnet Session")
            except EOFError:
                timer.sleep(5)
                tn = telnetConnect()
                line = tn.read_until(b"\n")
                logging.debug("It seems The previous session was closed so was used a new one.")

            splitted_line = str(line).split(';')
            if 'EVENT' in splitted_line[0]:
                logging.debug(line)
                try:
                    if splitted_line[2] in Switch:
                        manageRoom(splitted_line)
                    if splitted_line[2] in SwitchState:
                        changeSwitchState()
                except KeyError:
                    logging.debug("Key " + splitted_line[2] + " not in specific range")
    except (KeyboardInterrupt, SystemExit):
        logging.debug("The application was closed")
