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
            ac_value = DenormalizeAC(manufacturer, "set_temp", value)
        except Exception as e:
            print "Unsupported function or parameter (%s)" % e
            return

        if manufacturer == "atrea":
            # stats = self.elkonet.getStats(clim)
            # if "power" in stats:
            #     try:
            #         power = int(stats["power"])
            #         if power == 0:
            #             self.elkonet.setValue(clim, "power", 50)
            #     except:
            #         print 'Received bad power format from device'
            self.elkonet.setValue(clim, "requested_temperature", ac_value)

        elif manufacturer == "intesis":
            # self.elkonet.setValue(clim, "onoff", "on")
            self.elkonet.setValue(clim, "setptemp", ac_value)

        elif manufacturer == "airpohoda":
            pass

        elif manufacturer == "lg":
            # self.elkonet.setValue(clim, "power", True)
            self.elkonet.setValue(clim, "desired", ac_value)

        elif manufacturer == "coolmaster":
            # self.elkonet.setValue(clim, "OperationStatus", "ON")
            self.elkonet.setValue(clim, "SetTemp", ac_value)

        elif manufacturer == "universal":
            # self.elkonet.setValue(clim, "on/off", "1")
            self.elkonet.setValue(clim, "setTemp", ac_value)

        elif manufacturer == "nilan":
            # self.elkonet.setValue(clim, "on", True)
            self.elkonet.setValue(clim, "set temperature", ac_value)

        elif manufacturer == "daikin":
            self.elkonet.setValue(clim, "set_temp", ac_value)

        elif manufacturer == "mitsubishi":
            self.elkonet.setValue(clim, "set_temp", ac_value)

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