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
            self.elkonet.setValue(clim, "power", 50)

        elif manufacturer == "intesis":
            self.elkonet.setValue(clim, "onoff", "on")

        elif manufacturer == "airpohoda":
            stats = self.elkonet.getStats(clim)
            if "recuperation on/off" in stats:
                if not int(stats["recuperation on/off"]):
                    self.elkonet.setValue(clim, "powerOnOff", None)

        elif manufacturer == "lg":
            self.elkonet.setValue(clim, "power", True)

        elif manufacturer == "coolmaster":
            self.elkonet.setValue(clim, "OperationStatus", "ON")

        elif manufacturer == "universal":
            self.elkonet.setValue(clim, "on/off", "1")

        elif manufacturer == "nilan":
            self.elkonet.setValue(clim, "on", True)

        elif manufacturer == "daikin":
            self.elkonet.setValue(clim, "power", "on")

        elif manufacturer == "mitsubishi":
            self.elkonet.setValue(clim, "power", "on")

        elif manufacturer == "cairox":
            self.elkonet.setValue(clim, "power", "on")

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