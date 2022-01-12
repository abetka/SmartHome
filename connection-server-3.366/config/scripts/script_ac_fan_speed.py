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
            ac_value = DenormalizeAC(manufacturer, "fan_speed", value)
        except Exception as e:
            print "Unsupported function or parameter (%s)" % e
            return

        if manufacturer == "atrea":
            pass

        elif manufacturer == "intesis":
            # self.elkonet.setValue(clim, "onoff", "on")
            self.elkonet.setValue(clim, "fansp", ac_value)

        elif manufacturer == "airpohoda":
            pass

        elif manufacturer == "lg":
            # self.elkonet.setValue(clim, "power", True)
            self.elkonet.setValue(clim, "speed", ac_value)

        elif manufacturer == "coolmaster":
            # self.elkonet.setValue(clim, "OperationStatus", "ON")
            self.elkonet.setValue(clim, "FanSpeed", ac_value)

        elif manufacturer == "universal":
            pass

        elif manufacturer == "nilan":
            # self.elkonet.setValue(clim, "on", True)
            self.elkonet.setValue(clim, "speed fan", ac_value)

        elif manufacturer == "daikin":
            self.elkonet.setValue(clim, "fan_speed", ac_value)

        elif manufacturer == "mitsubishi":
            self.elkonet.setValue(clim, "fan_speed", ac_value)

        elif manufacturer == "cairox":
            self.elkonet.setValue(clim, "fan_speed_supply", ac_value)

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
        value = str(sys.argv[3])
    except:
        print 'Bad type of input arguments, terminating...'
        sys.exit(1)

    elkonet = Elkonet()
    elkonet.setValue(clim, manufacturer, value)