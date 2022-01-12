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
            pass

        elif manufacturer == "intesis":
            self.elkonet.setValue(clim, "onoff", "on")
            self.elkonet.setValue(clim, "mode", "heat")

        elif manufacturer == "airpohoda":
            pass

        elif manufacturer == "lg":
            self.elkonet.setValue(clim, "power", True)
            self.elkonet.setValue(clim, "mode", 4)

        elif manufacturer == "coolmaster":
            self.elkonet.setValue(clim, "OperationStatus", "ON")
            self.elkonet.setValue(clim, "OperationMode", "Heat")

        elif manufacturer == "universal":
            self.elkonet.setValue(clim, "on/off", "1")
            self.elkonet.setValue(clim, "heating", "1")

        elif manufacturer == "nilan":
            self.elkonet.setValue(clim, "on", True)
            self.elkonet.setValue(clim, "mode", 1)

        elif manufacturer == "daikin":
            self.elkonet.setValue(clim, "power", "on")
            self.elkonet.setValue(clim, "mode", "heating")

        elif manufacturer == "mitsubishi":
            self.elkonet.setValue(clim, "power", "on")
            self.elkonet.setValue(clim, "mode", "heating")

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