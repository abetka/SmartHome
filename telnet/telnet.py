import sys
import telnetlib
import logging
import threading
#--configuration
tn_ip = "192.168.88.246"
tn_port = "1111"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("telnet.log"),
        logging.StreamHandler()
    ]
)

def connect(host = tn_ip,port = tn_port):
    try:
        tn = telnetlib.Telnet(tn_ip, tn_port, 15)
    except BaseException as e:
        logging.error('Failed to connect to Telnet server: ' + str(e))
        return
    # tn.set_debuglevel(100)
    return tn

def getData( cmd, delimeter = ';'):
    tn = connect()
    try:
        tn.write(b"GET" + delimeter.encode('ascii') + cmd.encode('ascii') + b"\r\n")
        recv = tn.read_until(b"\r\n").decode('ascii').split(';')[2].rstrip("\r").rstrip("\n")
        logging.debug("Telnet GET Answer " + cmd + ": " + recv)
        tn.close()
        return int(recv)
    except BaseException as e:
        logging.error('Failed to GET value: ' + str(e))
        return 0

def setData( cmd, arg, delimeter = ';'):
    tn = connect()
    try:
        tn.write(b"SET" + delimeter.encode('ascii') + cmd.encode('ascii')+ delimeter.encode('ascii')+ arg.encode('ascii') + b"\r\n")
        recv = tn.read_until(b"\r\n").decode('ascii').split(';')[2].rstrip("\r").rstrip("\n")
        logging.debug("Telnet SET Answer " + cmd + ": " + recv)
        tn.close()
    except BaseException as e:
        logging.error('Failed to SET value: ' + str(e))

def dimmer(light,switch,tools):
    value = getData(tools[light])
    if switch:
        for i in range(100):
            setData(tools[light],str(i+1))
    else:
        for i in range(value):
            setData(tools[light],str(value - (i+1)))

def fanState(tools):
    try:
        state = {}
        for k, v in tools.items():
            state.update( { k: getData(v) } )
        logging.debug("Humidity: " + str((state['humidity']/100)))
        if state['fan'] == 1:
            if state['pointsLights'] == 1 or (state['humidity']/100) >= 40:
                setData(tools['fan'],'1')
                timer = threading.Timer( 100.0, fanState, [tools] )
                timer.start()
                logging.debug("Fan State of " + str(tools['fan']) + " is 1" )
                logging.debug(timer.is_alive())
            else:
                timer = threading.Timer( 100, setData, [tools['fan'],'0'] )
                timer.start()
                logging.debug("Fan State of " + str(tools['fan']) + " is 0" )
                logging.debug(timer.is_alive())
    except BaseException as e:
        logging.error('Failed to SET a FAN STATUS: ' + str(e))