#!/usr/bin/python


import sys
import time
import argparse
import traceback
import subprocess

from pyndn import Interest
from pyndn import Name
from pyndn import Face
from pyndn.security import KeyChain
from oscommand import OSCommand
from pyndn.util.blob import Blob


class Consumer(object):
    '''Hello '''

    def __init__(self, prefix):
        self.prefix = Name(prefix)
        self.outstanding = dict()  # a dictionary to keep track of outstanding Interests and retransmissions.
        self.isDone = False
        self.face = Face("127.0.0.1")
        # self.face = Face()
        self.keyChain = KeyChain()
        self.nodeid = OSCommand.getnodeid()

    def run(self):

        nodeid = OSCommand.getnodeid()
        subprocess.check_output(["export HOME=/tmp/minindn/{0} && nfdc route add / 260 ". \
                                format(nodeid)], shell=True)


        try:
            self._sendNextInterest(self.prefix)

            while not self.isDone:
                self.face.processEvents()
                time.sleep(0.01)

        except RuntimeError as e:
            print("ERROR: %s" % e)

    def _sendNextInterest(self, name):
        interest = Interest(name)
        uri = name.toUri()

        interest.setInterestLifetimeMilliseconds(5000)
        interest.setMustBeFresh(True)

        if uri not in self.outstanding:
            self.outstanding[uri] = 1
        self.face.expressInterest(interest, self._onData, self._onTimeout)

        print("========= Sent [ Interest ] ========= \n {0}\n \n".format(uri))

    def _onData(self, interest, data):
        payload = data.getContent()
        name = data.getName()

        print("========== Received [ data ] ========== ")
        print(payload.toRawStr())
        print("=======================================\n")

        del self.outstanding[name.toUri()]

        self.isDone = True

    def _onTimeout(self, interest):
        name = interest.getName()
        uri = name.toUri()

        print("TIMEOUT #%d: %s" % (self.outstanding[uri], uri))
        self.outstanding[uri] += 1

        if self.outstanding[uri] <= 3:
            self._sendNextInterest(name)
        else:
            self.isDone = True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse command line args for ndn consumer')
    parser.add_argument("-u", "--uri", required=True, help='ndn name to retrieve')
    args = parser.parse_args()

    try:
        uri = args.uri
        Consumer(uri).run()

    except:
        traceback.print_exc(file=sys.stdout)
        print("Error parsing command line arguments")
        sys.exit(1)
