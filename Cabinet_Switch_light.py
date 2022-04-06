
from telnet import telnet
import logging
from threading import Thread

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


def changeSwitchState():
    state = {}
    for k, v in switchTools.items():
        state.update( { k: telnet.getData(v) } )
    logging.debug(state)
    if state['chandelier'] == 0 and state['RGB_Red'] == 0 and state['RGB_Grean'] == 0 and state['RGB_Blue'] == 0:
        telnet.setData(switchSensor['Green3'],'1')
        telnet.setData(switchSensor['Red3'],'0')
    else:
        telnet.setData(switchSensor['Green3'],'0')
        telnet.setData(switchSensor['Red3'],'1')
    if state['backlightTable'] == 0 and state['curtainsCabinetOpen'] == 0 and state['curtainsCabinetClose'] == 0:
        telnet.setData(switchSensor['Green2'],'1')
        telnet.setData(switchSensor['Red2'],'0')
    else:
        telnet.setData(switchSensor['Green2'],'0')
        telnet.setData(switchSensor['Red2'],'1')
    if state['backlightWall'] == 0 and state['curtainsBigRoomOpen'] == 0 and state['curtainsBigRoomClose'] == 0:
        telnet.setData(switchSensor['Green1'],'1')
        telnet.setData(switchSensor['Red1'],'0')
    else:
        telnet.setData(switchSensor['Green1'],'0')
        telnet.setData(switchSensor['Red1'],'1')

def manageRoom(x):
    if x == switchSensor['Up1'] or x == switchImpulse['Push1']:
        telnet.setData(switchTools['chandelier'],'1')
    else:
        telnet.setData(switchTools['chandelier'],'0')
    if x == switchSensor['Up2'] or x == switchImpulse['Push2']:
        telnet.setData(switchTools['backlightTable'],'1')
    else:
        telnet.setData(switchTools['backlightTable'],'0')
    if x == switchSensor['Up3'] or x == switchImpulse['Push3']:
        telnet.setData(switchTools['backlightWall'],'1')
    else:
        telnet.setData(switchTools['backlightWall'],'0')
    if x == switchSensor['Down1']:
        t1 = Thread(telnet.dimmer('RGB_Red',True,switchTools))
        t2 = Thread(telnet.dimmer('RGB_Grean',True,switchTools))
        t3 = Thread(telnet.dimmer('RGB_Blue',True,switchTools))
        t1.start()
        t2.start()
        t3.start()
    else:
        t1 = Thread(telnet.dimmer('RGB_Red',False,switchTools))
        t2 = Thread(telnet.dimmer('RGB_Grean',False,switchTools))
        t3 = Thread(telnet.dimmer('RGB_Blue',False,switchTools))
        t1.start()
        t2.start()
        t3.start()
    if x == switchSensor['Down2']:
        telnet.setData(switchTools['curtainsCabinetOpen'],'1')
        telnet.setData(switchTools['curtainsCabinetOpen'],'0')
    else:
        telnet.setData(switchTools['curtainsCabinetClose'],'1')
        telnet.setData(switchTools['curtainsCabinetClose'],'0')
    if x == switchSensor['Down3']:
        telnet.setData(switchTools['curtainsBigRoomOpen'],'1')
        telnet.setData(switchTools['curtainsBigRoomOpen'],'0')
    else:
        telnet.setData(switchTools['curtainsBigRoomClose'],'1')
        telnet.setData(switchTools['curtainsBigRoomClose'],'0')

if __name__ == '__main__':
    try:
        tn = telnet.connect()
        while True:
            try:
                line = tn.read_until(b"\n")
                logging.debug("Used Current Telnet Session")
            except EOFError:
                time.sleep(5)
                tn = telnet.connect()
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
