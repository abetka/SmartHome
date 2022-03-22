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
from threading import Thread
#--configuration
tn_ip = "192.168.88.246"
tn_port = "1111"

switchTools = {
    'chandelier':'0x01020039',
    'backlightWall':'0x01020011',
    'backlightTable':'0x01020029',
    'curtainsCabinetOpen':'0x0102002f',
    'curtainsBigRoomOpen':'0x01020073',
    'curtainsCabinetClose':'0x01020026',
    'curtainsBigRoomClose':'0x01020072',
    'RGB_Red': '0x01040005',
    'RGB_Grean': '0x01040006',
    'RGB_Blue': '0x01040007',
    'RGB_Yellow': '0x01040008',
}
switchSensor = {
    'Up1': '0x01010039',
    'Down1': '0x0101003a',
    'Up2': '0x0101003b',
    'Down2': '0x0101003c',
    'Up3': '0x0101003d',
    'Down3': '0x0101003e',
    'Green1': '0x01020048',
    'Red1': '0x01020049',
    'Green2': '0x0102004a',
    'Red2': '0x0102004b',
    'Green3': '0x0102004c',
    'Red3': '0x0102004d',
    'Therm_Inter': '0x01050017',
    'Therm': '0x01050018',
    'DIN1': '0x0101003f',
    'DIN2': '0x01010040',
    'Light_In': '0x0102004e',
}
switchImpulse = {
    'Push1':'0x01010007',
    'Push2':'0x0101006f',
    'Push3':'0x01010004',
}
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("Cabinet_Switch_light.log"),
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
    state = {}
    for k, v in switchTools.items():
        state.update( { k: telnetGet(v) } )
    logging.debug(state)
    if state['chandelier'] == 0 and state['RGB_Red'] == 0 and state['RGB_Grean'] == 0 and state['RGB_Blue'] == 0:
        telnetSet(switchSensor['Green3'],'1')
        telnetSet(switchSensor['Red3'],'0')
    else:
        telnetSet(switchSensor['Green3'],'0')
        telnetSet(switchSensor['Red3'],'1')
    if state['backlightTable'] == 0 and state['curtainsCabinetOpen'] == 0 and state['curtainsCabinetClose'] == 0:
        telnetSet(switchSensor['Green2'],'1')
        telnetSet(switchSensor['Red2'],'0')
    else:
        telnetSet(switchSensor['Green2'],'0')
        telnetSet(switchSensor['Red2'],'1')
    if state['backlightWall'] == 0 and state['curtainsBigRoomOpen'] == 0 and state['curtainsBigRoomClose'] == 0:
        telnetSet(switchSensor['Green1'],'1')
        telnetSet(switchSensor['Red1'],'0')
    else:
        telnetSet(switchSensor['Green1'],'0')
        telnetSet(switchSensor['Red1'],'1')

def dimmer(light,switch):
    value = telnetGet(switchTools[light])
    if switch:
        for i in range(100):
            telnetSet(switchTools[light],str(i+1))
    else:
        for i in range(value):
            telnetSet(switchTools[light],str(value - (i+1)))

def manageRoom(x):
    if x == switchSensor['Up1'] or x == switchImpulse['Push1']:
        telnetSet(switchTools['chandelier'],'1')
    else:
        telnetSet(switchTools['chandelier'],'0')
    if x == switchSensor['Up2'] or x == switchImpulse['Push2']:
        telnetSet(switchTools['backlightTable'],'1')
    else:
        telnetSet(switchTools['backlightTable'],'0')
    if x == switchSensor['Up3'] or x == switchImpulse['Push3']:
        telnetSet(switchTools['backlightWall'],'1')
    else:
        telnetSet(switchTools['backlightWall'],'0')
    if x == switchSensor['Down1']:
        t1 = Thread(dimmer('RGB_Red',True))
        t2 = Thread(dimmer('RGB_Grean',True))
        t3 = Thread(dimmer('RGB_Blue',True))
        t1.start()
        t2.start()
        t3.start()
    else:
        t1 = Thread(dimmer('RGB_Red',False))
        t2 = Thread(dimmer('RGB_Grean',False))
        t3 = Thread(dimmer('RGB_Blue',False))
        t1.start()
        t2.start()
        t3.start()
    if x == switchSensor['Down2']:
        telnetSet(switchTools['curtainsCabinetOpen'],'1')
        telnetSet(switchTools['curtainsCabinetOpen'],'0')
    else:
        telnetSet(switchTools['curtainsCabinetClose'],'1')
        telnetSet(switchTools['curtainsCabinetClose'],'0')
    if x == switchSensor['Down3']:
        telnetSet(switchTools['curtainsBigRoomOpen'],'1')
        telnetSet(switchTools['curtainsBigRoomOpen'],'0')
    else:
        telnetSet(switchTools['curtainsBigRoomClose'],'1')
        telnetSet(switchTools['curtainsBigRoomClose'],'0')

if __name__ == '__main__':
    try:
        tn = telnetConnect()
        while True:
            try:
                line = tn.read_until(b"\n")
                logging.debug("Used Current Telnet Session")
            except EOFError:
                time.sleep(5)
                tn = telnetConnect()
                line = tn.read_until(b"\n")
                logging.debug("It seems The previous session was closed so was used a new one.")

            splitted_line = str(line).split(';')
            if 'EVENT' in splitted_line[0]:
                logging.debug(line)
                try:
                    if splitted_line[2] in switchSensor:
                        manageRoom(splitted_line)
                    if splitted_line[2] in switchImpulse:
                        manageRoom(splitted_line)
                    if splitted_line[2] in switchTools.values():
                        changeSwitchState()
                except KeyError:
                    logging.debug("Key " + splitted_line[2] + " not in specific range")
    except (KeyboardInterrupt, SystemExit):
        logging.debug("The application was closed")
