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

def telnetConnect(host = tn_ip,port = tn_port):
    try:
        tn = telnetlib.Telnet(tn_ip, tn_port, 15)
    except:
        logging.debug("Unable to connect to Telnet server: " + tn_ip)
        # print("Unable to connect to Telnet server: " + tn_ip)
        return
    tn.set_debuglevel(100)
    return tn

def telnetGet( cmd, delimeter = ';'):
    tn = telnetConnect()
    tn.write(b"GET" + delimeter.encode('ascii') + cmd.encode('ascii') + b"\r\n")
    recv = tn.read_until(b"\r\n").decode('ascii').split(';')[2].rstrip("\r").rstrip("\n")
    logging.debug("Telnet GET Answer" + cmd + ": " + recv)
    tn.close()

def telnetSet( cmd, arg, delimeter = ';'):
    tn = telnetConnect()
    tn.write(b"SET" + delimeter.encode('ascii') + cmd.encode('ascii')+ delimeter.encode('ascii')+ arg.encode('ascii') + b"\r\n")
    recv = tn.read_until(b"\r\n").decode('ascii').split(';')[2].rstrip("\r").rstrip("\n")
    logging.debug("Telnet SET Answer" + cmd + ": " + recv)
    tn.close()


if __name__ == '__main__':

    telnetGet('0x0102006e')
    telnetGet('0x0102006f')
    telnetSet('0x0102006e','1')
    time.sleep(30)
    telnetSet('0x0102006e','0')
    telnetSet('0x0102006f','1')
    time.sleep(30)
    telnetSet('0x0102006f','0')
    # telnetSet('0x0102002f','1')
    # telnetSet('0x0102002f','0')


#     EVENT;05;0x02030009;1
# EVENT;05;0x0102002f;1
# NOP
# NOP
# EVENT;06;0x02030009;0
# EVENT;06;0x0102002f;0
# EVENT;05;0x0203000a;1
# EVENT;05;0x01020026;1

    logging.debug('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
