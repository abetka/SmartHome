import sys
import xmlrpclib
import json


"""

argv1 - STRING - clim name
argv2 - STRING - clim manufacturer
argv3 - INT - value for function

"""


IP = "localhost"


class Elkonet():
    def __init__(self):
        self.elkonet = xmlrpclib.Server("http://{}:8001".format(IP))

    def setValue(self, clim, manufacturer, value):

        if manufacturer == "atrea":
            stats = self.elkonet.getStats(clim)
            if "power" in stats:
                try:
                    power = int(stats["power"])
                    if power == 0:
                        self.elkonet.setValue(clim, "power", 50)
                except:
                    print 'Received bad power format from device'
            if "requested_temperature" in stats:
                try:
                    temp = int(float(stats["requested_temperature"]))
                    self.elkonet.setValue(clim, "requested_temperature", temp + 1)
                except:
                    print 'Received bad temperature format from device'

        elif manufacturer == "intesis":
            self.elkonet.setValue(clim, "onoff", "on")
            stats = self.elkonet.getStats(clim)
            if "setptemp" in stats:
                try:
                    temp = int(float(stats["setptemp"]))
                    self.elkonet.setValue(clim, "setptemp", str(temp + 10))
                except:
                    print 'Received bad temperature format from device'

        elif manufacturer == "airpohoda":
            stats = self.elkonet.getStats(clim)
            if "recuperation on/off" in stats:
                if not int(stats["recuperation on/off"]):
                    self.elkonet.setValue(clim, "powerOnOff", None)
            self.elkonet.setValue(clim, "up", None)

        elif manufacturer == "lg":
            self.elkonet.setValue(clim, "power", True)
            stats = self.elkonet.getStats(clim)
            if "desired" in stats:
                try:
                    temp = int(float(stats["desired"]))
                    self.elkonet.setValue(clim, "desired", temp + 1)
                except:
                    print 'Received bad temperature format from device'

        elif manufacturer == "coolmaster":
            self.elkonet.setValue(clim, "OperationStatus", "ON")
            stats = self.elkonet.getStats(clim)
            if "SetTemp" in stats:
                try:
                    temp = int(float(stats["SetTemp"][:-1]))
                    self.elkonet.setValue(clim, "SetTemp", temp + 1)
                except:
                    print 'Received bad temperature format from device'

        elif manufacturer == "universal":
            self.elkonet.setValue(clim, "on/off", "1")
            stats = self.elkonet.getStats(clim)
            if "setTemp" in stats:
                try:
                    temp = int(float(stats["setTemp"]))
                    self.elkonet.setValue(clim, "setTemp", str(temp + 1))
                except:
                    print 'Received bad temperature format from device'

        elif manufacturer == "nilan":
            self.elkonet.setValue(clim, "on", True)
            stats = self.elkonet.getStats(clim)
            if "state" in stats:
                if "set temperature" in stats["state"]:
                    try:
                        temp = int(float(stats["state"]["set temperature"]))
                        self.elkonet.setValue(clim, "set temperature", temp + 1)
                    except:
                        print 'Received bad temperature format from device'

        elif manufacturer == "daikin":
            self.elkonet.setValue(clim, "power", "on")
            stats = self.elkonet.getStats(clim)
            if "set_temp" in stats:
                try:
                    temp = int(float(stats["set_temp"]))
                    self.elkonet.setValue(clim, "set_temp", temp + 1)
                except:
                    print 'Received bad temperature format from device'

        elif manufacturer == "mitsubishi":
            self.elkonet.setValue(clim, "power", "on")
            stats = self.elkonet.getStats(clim)
            if "set_temp" in stats:
                try:
                    temp = int(float(stats["set_temp"]))
                    self.elkonet.setValue(clim, "set_temp", temp + 1)
                except:
                    print 'Received bad temperature format from device'

        elif manufacturer == "cairox":
            pass

        else:
            print 'Bad manufacturer name'
            return

        print 'Clim set'


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print 'Bad count of input arguments, terminating...'
        sys.exit(1)

    try:
        clim = sys.argv[1]
        manufacturer = sys.argv[2].lower()
        value = int(sys.argv[3])
    except:
        print 'Bad type of input arguments, terminating...'
        sys.exit(1)

    elkonet = Elkonet()
    elkonet.setValue(clim, manufacturer, value)