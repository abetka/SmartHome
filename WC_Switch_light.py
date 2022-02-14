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

def fanState(x):
    fan = telnetGet(x['fan'])
    lightState = telnetGet(x['light'])
    humidityState = telnetGet(x['humidity'])/100
    logging.debug("lightState is " + str(lightState) )
    logging.debug("humidityState is " + str(humidityState) )
    if fan == 1:
        if lightState == 1 or humidityState >= 30:
            telnetSet(x['fan'],'1')
            timer = threading.Timer( 100.0, fanState, [x] )
            timer.start()
            logging.debug("Fan State of " + x['fan'] + " is 1" )
            logging.debug(timer.is_alive())
        else:
            timer = threading.Timer( 100, telnetSet, [x['fan'],'0'] )
            timer.start()
            logging.debug("Fan State of " + x['fan'] + " is 0" )
            logging.debug(timer.is_alive())

def changeWCSwitchState():
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
def manageWCRoom(x):
# WC_Switch_Up1 GSB3-40_Up1_026A2E 0x01010047 0x00000000
# WC_Switch_Down1 GSB3-40_Down1_026A2E 0x01010048 0x00000000
# WC_Switch_Up2 GSB3-40_Up2_026A2E 0x01010049 0x00000000
# WC_Switch_Down2 GSB3-40_Down2_026A2E 0x0101004A 0x00000000
# WC_Switch_Inside_Up WSB3-20-Hum_Up_02594C 0x01010019 0x00000000
# WC_Switch_Inside_Down WSB3-20-Hum_Down_02594C 0x0101001A 0x00000000
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
        WCSwitchState = [
            '0x0102002e',
            '0x01020025',
            '0x01020003',
            '0x01020014',
        ]
        WCSwitch = [
            '0x01010047',
            '0x01010048',
            '0x01010049',
            '0x0101004a',
            '0x01010019',
            '0x0101001a',
            '0x0101000a',
        ]
        CurtainsState = [
            '0x01020072',
            '0x01020073',
            '0x01020074',
            '0x01020075',
            '0x0102006e',
            '0x0102006f',
            '0x01020070',
            '0x01020071',
            '0x01020076',
            '0x01020077',
            '0x01020078',
            '0x01020079',
            '0x01020026',
            '0x0102002f',
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
                    if splitted_line[2] in WCSwitch:
                        manageWCRoom(splitted_line)
                    if splitted_line[2] in WCSwitchState:
                        changeWCSwitchState()
                    if splitted_line[2] in CurtainsState:
                        changeCurtainsState(splitted_line)
                    if splitted_line[2] == '0x01020025':
                        listofX = {
                            'fan':'0x01020025',
                            'light':'0x0102002e',
                            'humidity':'0x01050009',
                        }
                        fanState(listofX)
                except KeyError:
                    logging.debug("Key " + splitted_line[2] + " not in specific range")
    except (KeyboardInterrupt, SystemExit):
        logging.debug("The application was closed")
