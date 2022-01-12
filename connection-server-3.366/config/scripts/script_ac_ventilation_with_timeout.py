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

        if value == 0 or value > 30:
            return

        if manufacturer == "atrea":
            self.elkonet.setValue(clim, "ventilation_with_timeout", value)

        elif manufacturer == "intesis":
            self.elkonet.setValue(clim, "ventilation_with_timeout", value)

        elif manufacturer == "airpohoda":
            pass

        elif manufacturer == "lg":
            self.elkonet.setValue(clim, "ventilation_with_timeout", value)

        elif manufacturer == "coolmaster":
            self.elkonet.setValue(clim, "ventilation_with_timeout", value)

        elif manufacturer == "universal":
            pass

        elif manufacturer == "nilan":
            self.elkonet.setValue(clim, "boost", value)

        elif manufacturer == "daikin":
            self.elkonet.setValue(clim, "ventilation_with_timeout", value)

        elif manufacturer == "mitsubishi":
            self.elkonet.setValue(clim, "ventilation_with_timeout", value)

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