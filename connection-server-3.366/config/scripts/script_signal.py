import sys
import xmlrpclib
import time
import json


"""

argv1 - JSON "{'uid': value, 'uid': value, ...}"
argv2 - JSON "{'uid': value, 'uid': value, ...}"
argv3 - Time of signal duration

"""


IP = "localhost"


class Elkonet():
    def __init__(self):
        self.elkonet = xmlrpclib.Server("http://{}:8001".format(IP))

    def set(self, values):
        self.elkonet.writeValuesByAddress(values)
        print 'Values set'


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print 'Bad count of input arguments, terminating...'
        sys.exit(1)

    try:
        value_1 = json.loads(sys.argv[1])
        value_2 = json.loads(sys.argv[2])
        duration = int(sys.argv[3])
    except:
        print 'Bad type of input arguments, terminating...'
        sys.exit(1)

    elkonet = Elkonet()
    elkonet.set(value_1)
    time.sleep(duration)
    elkonet.set(value_2)

