
from telnet import telnet
import logging

switchTools = {
    'mirror':'0x01020003',
    'backlight':'0x01020014',
    'fan':'0x01020025',
    'pointsLights':'0x0102002e',
    'humidity': '0x01050009',
    'waterleak': '0x01020027',
}
switchSensor = {
    'Up1': '0x01010047',
    'Down1': '0x01010048',
    'Up2': '0x01010049',
    'Down2': '0x0101004a',
    'Up3': '0x01010019',
    'Down3': '0x0101001a',
    'Green1': '0x01020053',
    'Red1': '0x01020054',
    'Green2': '0x01020055',
    'Red2': '0x01020056',
    'Green3': '0x0102001d',
    'Red3': ' 0x0102001e',
    'Humidity': '0x01050006',
    'Therm': '0x01050008',
    'Therm_Inter': '0x01050007',
    'waterleak': '0x0101000a',
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
    if state['mirror'] == 0 and state['backlight'] == 0 and state['fan'] == 0:
        telnet.setData(switchSensor['Green3'],'1')
        telnet.setData(switchSensor['Red3'],'0')
    else:
        telnet.setData(switchSensor['Green3'],'0')
        telnet.setData(switchSensor['Red3'],'1')
    if state['mirror'] == 0 and state['backlight'] == 0:
        telnet.setData(switchSensor['Green2'],'1')
        telnet.setData(switchSensor['Red2'],'0')
    else:
        telnet.setData(switchSensor['Green2'],'0')
        telnet.setData(switchSensor['Red2'],'1')
    if state['pointsLights'] == 0 and state['fan'] == 0:
        telnet.setData(switchSensor['Green1'],'1')
        telnet.setData(switchSensor['Red1'],'0')
    else:
        telnet.setData(switchSensor['Green1'],'0')
        telnet.setData(switchSensor['Red1'],'1')

def manageRoom(x):
    state = {}
    for k, v in switchTools.items():
        state.update( { k: telnet.getData(v) } )
    logging.debug(state)
    if int(x[1]) == 29 and int(x[3][:-5]) == 1:
        if x[2] == switchSensor['Up1']:
            if state['pointsLights'] == 0:
                telnet.setData(switchTools['pointsLights'],'1')
            else:
                telnet.setData(switchTools['pointsLights'],'0')
            if state['fan'] == 0 and state['pointsLights'] == 0:
                telnet.setData(switchTools['fan'],'1')
#======================================================
        if x[2] == switchSensor['Down1'] or x[2] == switchSensor['Down3']:
            if state['fan'] == 0:
                telnet.setData(switchTools['fan'],'1')
            else:
                telnet.setData(switchTools['fan'],'0')
#======================================================
        if x[2] == switchSensor['Up2'] or x[2] == switchSensor['Up3']:
            if state['mirror'] == 0:
                telnet.setData(switchTools['mirror'],'1')
            else:
                telnet.setData(switchTools['mirror'],'0')
            if state['backlight'] == 0:
                telnet.setData(switchTools['backlight'],'1')
            else:
                telnet.setData(switchTools['backlight'],'0')
#======================================================
        if x[2] == switchSensor['Down2']:
            for k, v in switchTools.items():
                if k != 'humidity' or k != 'waterleak':
                    telnet.setData(v,'0')
#======================================================
        if x[2] == switchSensor['waterleak']:
            telnet.setData(switchTools['waterleak'],'1')
#======================================================
    if int(x[1]) == 30 and int(x[3][:-5]) == 0:
        if x[2] == switchSensor['waterleak']:
            telnet.setData(switchTools['waterleak'],'0')

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
                    if splitted_line[2] in switchSensor.values():
                        manageRoom(splitted_line)
                    if splitted_line[2] in switchTools.values():
                        changeSwitchState()
                    if splitted_line[2] == switchTools['fan']:
                        telnet.fanState(switchTools)
                except KeyError:
                    logging.debug("Key " + splitted_line[2] + " not in specific range")
    except (KeyboardInterrupt, SystemExit):
        logging.debug("The application was closed")
