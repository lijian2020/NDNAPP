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

'''This module is used for test. It works as a data producer (Server). It listen to  incoming Interest message of
a specific prefix send send back Data.
the compulsive argument '-n' has to be set and followed by a prefix that you want to listen to. You can use the
command like this to run is:
python3 testproducer.py -n /ndn/aaaa/bbbb
'''


import sys
import time
import argparse
import traceback
import random

from pyndn import Name
from pyndn import Data
from pyndn import Face
from pyndn.security import KeyChain


class Producer(object):
    def __init__(self):
        self.keyChain = KeyChain()
        self.isDone = False

    def run(self, namespace):
        # Create a connection to the local forwarder over a Unix socket
        face = Face()
        prefix = Name(namespace)

        # Use the system default key chain and certificate name to sign commands.
        face.setCommandSigningInfo(self.keyChain, \
                                   self.keyChain.getDefaultCertificateName())

        # Also use the default certificate name to sign Data packets.
        '''Register prefix with the connected NDN hub and call onInterest when a
        matching interest is received. To register a prefix with NFD, you must
        first call setCommandSigningInfo.'''
        face.registerPrefix(prefix, self.onInterest, self.onRegisterFailed)

        print("Registering prefix", prefix.toUri())

        # Run the event loop forever. Use a short sleep to
        # prevent the Producer from using 100% of the CPU.
        while not self.isDone:
            face.processEvents()
            time.sleep(0.01)

    def onInterest(self, prefix, interest, transport, registeredPrefixId):
        print("========= received [ interest ] ========= :\n" + interest.getName().toUri())  # for test
        interestName = interest.getName()
        appcontentstr = interest.getApplicationParameters()

        data = Data(interestName)
        data.setContent("Hello! This data come from producer-01.")

        # hourMilliseconds = 3600 * 1000
        hourMilliseconds = 0  # here I should set it 0 since it always need to fresh.

        data.getMetaInfo().setFreshnessPeriod(hourMilliseconds)
        self.keyChain.sign(data, self.keyChain.getDefaultCertificateName())
        transport.send(data.wireEncode().toBuffer())
        print("\n ######## Replied [ data ] ########\n \n")

    def onRegisterFailed(self, prefix):
        print("Register failed for prefix", prefix.toUri())
        self.isDone = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse command line args for ndn producer')
    parser.add_argument("-n", "--namespace", required=True, help='namespace to listen under')

    args = parser.parse_args()

    try:
        namespace = args.namespace
        Producer().run(namespace)

    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)
