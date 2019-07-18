#!/usr/bin/python3
#
# Copyright (C) 2019 Trinity College of Dublin, the University of Dublin.
# Copyright (c) 2019 Li Jian
# Author: Li Jian <lij12@tcd.ie>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


'''This module is used for test. It works as a data consumer (Client) and sends Interest message to a specific prefix.
the compulsive argument '-u' has to be set and followed by a prefix you want to send the interest to.
You can use the command like this to run it:
python3 testconsumer.py -u /ndn/aaaa/bbbb
'''


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

        interest.setInterestLifetimeMilliseconds(10000)
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
