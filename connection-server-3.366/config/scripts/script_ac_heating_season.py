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
            ac_value = DenormalizeAC(manufacturer, "heating_season", value)
        except Exception as e:
            print "Unsupported function or parameter (%s)" % e
            return

        if manufacturer == "atrea":
            self.elkonet.setValue(clim, "heating_season", ac_value)

        elif manufacturer == "intesis":
            pass

        elif manufacturer == "airpohoda":
            pass

        elif manufacturer == "lg":
            pass

        elif manufacturer == "coolmaster":
            pass

        elif manufacturer == "universal":
            pass

        elif manufacturer == "nilan":
            pass

        elif manufacturer == "daikin":
            pass

        elif manufacturer == "mitsubishi":
            pass

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