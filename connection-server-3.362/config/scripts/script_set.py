import sys
import xmlrpclib
import json


"""

argv1 - JSON "{'uid': value, 'uid': value, ...}"

"""


IP = "localhost"


class Elkonet():
    def __init__(self):
        self.elkonet = xmlrpclib.Server("http://{}:8001".format(IP))

    def set(self, values):
        self.elkonet.writeValuesByAddress(values)
        print 'Values set'


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print 'Bad count of input arguments, terminating...'
        sys.exit(1)

    try:
        value_1 = json.loads(sys.argv[1])
    except:
        print 'Bad type of input arguments, terminating...'
        sys.exit(1)

    elkonet = Elkonet()
    elkonet.set(value_1)