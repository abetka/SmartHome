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
    logging.debug("Telnet GET Answer" + cmd + ": " + recv)
    tn.close()

def telnetSet( cmd, arg, delimeter = ';'):
    tn = telnetConnect()
    tn.write(b"SET" + delimeter.encode('ascii') + cmd.encode('ascii')+ delimeter.encode('ascii')+ arg.encode('ascii') + b"\r\n")
    recv = tn.read_until(b"\r\n").decode('ascii').split(';')[2].rstrip("\r").rstrip("\n")
    logging.debug("Telnet SET Answer" + cmd + ": " + recv)
    tn.close()

def sunTime(type,date=date.today()):
    cityInfo = LocationInfo(city, country, timezone)
    s = sun(cityInfo.observer, date=date, tzinfo=cityInfo.timezone)
    logging.debug(type)
    logging.debug(s)
    return s[type]

def closeCurtains(scheduler):
    for x in close_curtains:
        telnetSet(x,"1")
        logging.debug("Will be closed " + x)
    scheduler.add_job(closeCurtains, 'date', run_date=sunTime("sunset",date.today() + timedelta(days = 1)), args=[scheduler] )
    logging.debug(scheduler.print_jobs())

def openCurtains(scheduler):
    for x in open_curtains:
        telnetSet(x,"1")
        logging.debug("Will be opened " + x)
    scheduler.add_job(openCurtains, 'date', run_date=sunTime("sunrise",date.today() + timedelta(days = 1, hours = 1)), args=[scheduler] )
    logging.debug(scheduler.print_jobs())


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(closeCurtains, 'date', run_date=datetime.now() + timedelta(minutes = 3 ), args=[scheduler] )
    scheduler.add_job(openCurtains, 'date', run_date=datetime.now() + timedelta(minutes = 5 ), args=[scheduler] )
    logging.debug(scheduler.print_jobs())
    scheduler.start()
    logging.debug('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
