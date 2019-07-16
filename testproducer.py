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
