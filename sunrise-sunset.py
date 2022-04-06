
import os
import logging
import time
from telnet import telnet
from threading import Thread
from suntime import Sun, SunTimeException
from datetime import datetime
from datetime import date
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler

curtains = {
   'cabinet': {
       'close': '0x01020026',
       'open': '0x0102002f',
   },
   'bigRoom': {
       'close': '0x01020072',
       'open': '0x01020073',
   },
   'smallRoom': {
       'close': '0x0102006f',
       'open': '0x0102006e',
   },
   'kitchen': {
       'close': '0x01020077',
       'open': '0x01020076',
   },
}

Latitude = 46.28
Longitude = 30.43

#===========================

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("Cabinet_Switch_light.log"),
        logging.StreamHandler()
    ]
)


def sunTime(type,date=date.today()):
    sun = Sun(Latitude, Longitude)
    s = {
        'sunrise': sun.get_local_sunrise_time(date),
        'sunset': sun.get_local_sunset_time(date),
    }
    logging.debug(type)
    logging.debug(s)
    return s[type]

def curtainsAction(type):
    for k,v in curtains.items():
        telnet.setData(v[type],'1')
        time.sleep(5)
        telnet.setData(v[type],'0')
        logging.debug(k + " curtain will be " + type + " " + v[type])

def closeCurtains(scheduler):
    curtainsAction('close')
    scheduler.add_job(closeCurtains, 'date', run_date=sunTime("sunset",date.today() + timedelta(days = 1)), args=[scheduler] )
    logging.debug(scheduler.print_jobs())

def openCurtains(scheduler):
    curtainsAction('open')
    scheduler.add_job(openCurtains, 'date', run_date=sunTime("sunrise",date.today() + timedelta(days = 1 ))  + timedelta( minutes = 30 ), args=[scheduler] )
    logging.debug(scheduler.print_jobs())

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    try:
        logging.debug(sunTime("sunset",date.today() + timedelta(days = 1)))
        logging.debug(sunTime("sunrise",date.today() + timedelta(days = 1, minutes = 30 )))
        scheduler.add_job(closeCurtains, 'date', run_date=sunTime("sunset",date.today() + timedelta(days = 1 )), args=[scheduler] )
        scheduler.add_job(openCurtains, 'date', run_date=sunTime("sunrise",date.today() + timedelta(days = 1 )) + timedelta( minutes = 30 ), args=[scheduler] )
        logging.debug(scheduler.print_jobs())
        scheduler.start()
        logging.debug('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
