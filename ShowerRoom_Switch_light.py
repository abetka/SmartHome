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
        logging.FileHandler("ShowerRoom_Switch_light.log"),
        logging.StreamHandler()
    ]
)

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

def changeSwitchState():
    pointLights = telnetGet("0x0102000b")
    fan = telnetGet("0x01020024")
    backLightMirror = telnetGet("0x01020001")
    backLight = telnetGet("0x01020012")
    if pointLights == 0 and fan == 0:
        telnetSet("0x01020017","1") #green1
        telnetSet("0x01020018","0") #red1
    else:
        telnetSet("0x01020017","0") #green1
        telnetSet("0x01020018","1") #red1
    if backLightMirror == 0 and backLight == 0:
        telnetSet("0x01020015","1") #green2
        telnetSet("0x01020016","0") #red2
    else:
        telnetSet("0x01020015","0") #green2
        telnetSet("0x01020016","1") #red2
    if backLightMirror == 0 and backLight == 0 and fan == 0:
        telnetSet("0x0102001B","1") #green inside
        telnetSet("0x0102001C","0") #red inside
    else:
        telnetSet("0x0102001B","0") #green inside
        telnetSet("0x0102001C","1") #red inside


def manageRoom(x):
    logging.debug("managedWCSwitch ")
    print(x)
    pointLights = telnetGet("0x0102000b")
    fan = telnetGet("0x01020024")
    backLights = telnetGet("0x01020012")
    mirrorLights = telnetGet("0x01020001")
    fanSwitch = ['0x01010012', '0x01010016']
    lightSwitch = ['0x0101000f', '0x01010015']

    # Up2
    if int(x[1]) == 29 and x[2] == '0x01010011' and int(x[3][:-5]) == 1:
        if pointLights == 0:
            telnetSet("0x0102000b","1")
        else:
            telnetSet("0x0102000b","0")
        if fan == 0 and pointLights == 0:
            telnetSet('0x01020024','1')
    # Down2 Down1 inside
    if int(x[1]) == 29 and x[2] in fanSwitch and int(x[3][:-5]) == 1:
        if fan == 0:
            telnetSet('0x01020024','1')
        else:
            telnetSet('0x01020024','0')
    # Up1 Up1 inside
    if int(x[1]) == 29 and x[2] in lightSwitch and int(x[3][:-5]) == 1:
        if backLights == 0:
            telnetSet("0x01020012","1")
        else:
            telnetSet("0x01020012","0")
        if mirrorLights == 0:
            telnetSet("0x01020001","1")
        else:
            telnetSet("0x01020001","0")
    # Down2
    if int(x[1]) == 29 and x[2] == '0x01010010' and int(x[3][:-5]) == 1:
        telnetSet("0x0102000b","0")
        telnetSet("0x01020012","0")
        telnetSet("0x01020001","0")
        telnetSet('0x01020024','0')

if __name__ == '__main__':
    try:
        tn = telnetConnect()
        SwitchState = [
            '0x01020001', #Bathroom_Backlight
            '0x0102000b', #Bathroom_Points_Lights
            '0x01020012', #Bathroom_Niche
            '0x01020024', #Bathroom_Fan
        ]
        Switch = [
            '0x0101000f', #Bathroom_Switch_Up1
            '0x01010010', #Bathroom_Switch_Down1
            '0x01010011', #Bathroom_Switch_Up2
            '0x01010012', #Bathroom_Switch_Down2
            '0x01010015', #Bathroom_Switch_Inside_Up
            '0x01010016', #Bathroom_Switch_Inside_Down
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
                    if splitted_line[2] == '0x01020024':
                        listofX = {
                            'fan':'0x01020024',
                            'light':'0x0102000b',
                            'humidity':'0x01050006',
                        }
                        fanState(listofX)
                except KeyError:
                    logging.debug("Key " + splitted_line[2] + " not in specific range")
    except (KeyboardInterrupt, SystemExit):
        logging.debug("The application was closed")
