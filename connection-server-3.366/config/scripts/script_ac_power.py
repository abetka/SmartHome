import sys
import xmlrpclib
import json

from normalizer.normalizer import DenormalizeAC

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

        try:
            ac_value = DenormalizeAC(manufacturer, "power", value)
        except Exception as e:
            print "Unsupported function or parameter (%s)" % e
            return

        if manufacturer == "atrea":
            self.elkonet.setValue(clim, "power", 100 if ac_value == 1 else ac_value)

        elif manufacturer == "intesis":
            self.elkonet.setValue(clim, "onoff", ac_value)

        elif manufacturer == "airpohoda":
            stats = self.elkonet.getStats(clim)
            if "recuperation on/off" in stats:
                if not stats["recuperation on/off"] == ac_value:
                    self.elkonet.setValue(clim, "powerOnOff", None)

        elif manufacturer == "lg":
            self.elkonet.setValue(clim, "power", ac_value)

        elif manufacturer == "coolmaster":
            self.elkonet.setValue(clim, "OperationStatus", ac_value)

        elif manufacturer == "universal":
            self.elkonet.setValue(clim, "on/off", ac_value)

        elif manufacturer == "nilan":
            self.elkonet.setValue(clim, "on", ac_value)

        elif manufacturer == "daikin":
            self.elkonet.setValue(clim, "power", ac_value)

        elif manufacturer == "mitsubishi":
            self.elkonet.setValue(clim, "power", ac_value)

        elif manufacturer == "cairox":
            self.elkonet.setValue(clim, "power", ac_value)

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