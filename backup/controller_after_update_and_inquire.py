# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2014 Regents of the University of California.
# Copyright (c) 2014 Susmit Shannigrahi, Steve DiBenedetto
#
# Author: Jeff Thompson <jefft0@remap.ucla.edu>
# Author Steve DiBenedetto <http://www.cs.colostate.edu/~dibenede>
# Author Susmit Shannigrahi <http://www.cs.colostate.edu/~susmit>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# A copy of the GNU General Public License is in the file COPYING.

import sys
import time
import argparse
import traceback
import subprocess
import ofmsg
import random

from pyndn import Name
from pyndn import Data
from pyndn import Face
from pyndn.security import KeyChain

#TODO(lijian): change the class name to controller
class Producer(object):
    def __init__(self):
        self.keyChain = KeyChain()
        self.isDone = False
        self.PRT = ofmsg.PrefixRouteTable()

    def run(self):
        # Create a connection to the local forwarder over a Unix socket
        face = Face()
        mainPrefixString = '/ndn/ie/tcd/controller01/'
        updatePRTPrefixString = '/ndn/ie/tcd/controller01/update/'
        inquirePRTPrefixString = '/ndn/ie/tcd/controller01/inquire/'
        mainPrefix = Name(mainPrefixString)
        updatePRTPrefix = Name(updatePRTPrefixString)
        inquirePRTPrefix = Name(inquirePRTPrefixString)

        subprocess.call(["export HOME=/tmp/minindn/h6 && nlsrc advertise {} ".\
                                        format(mainPrefixString)],shell=True)


        # Use the system default key chain and certificate name to sign commands.
        face.setCommandSigningInfo(self.keyChain, \
                                   self.keyChain.getDefaultCertificateName())

        # Also use the default certificate name to sign Data packets.
        '''Register prefix with the connected NDN hub and call onInterest when a
        matching interest is received. To register a prefix with NFD, you must
        first call setCommandSigningInfo.'''
        # here I need to register an aggregated prefix,like "/controller"
        #face.registerPrefix(prefix, self.onInterest, self.onRegisterFailed)
        face.registerPrefix(mainPrefix, self.onInterest_Mian, self.onRegisterFailed) #main prefix
        print("Registering prefix", mainPrefixString)

        #filters:
        #This filter won't register prefix,but can give different reponse according to prefix
        #like "/controller/a", "/controller/b",...and use 'self.onInterest-a', 'self.onInterest-b'...
        face.setInterestFilter(updatePRTPrefix,self.onInterest_Update)   #for updating PRT
        face.setInterestFilter(inquirePRTPrefix, self.onInterest_Inquire)  # for inquiring PRT


        # Run the event loop forever. Use a short sleep to
        # prevent the Producer from using 100% of the CPU.
        while not self.isDone:
            face.processEvents()
            time.sleep(0.01)

    def onInterest_Mian(self, mainPrefix, interest, transport, registeredPrefixId):
        #TODO(lijian): check what should do.
        pass

    def onInterest_Update(self,prifix,interest,transport,registeredPrefixId):
        returndatacontent=self.PRT.updatenodeprefixtable(interest)
        data=self.set_returndata(interest, returndatacontent)
        transport.send(data.wireEncode().toBuffer())


    def onInterest_Inquire(self,prifix,interest,transport,registeredPrefixId):
        parsed_interest = self.PRT.parseinterest(interest)
        index_number = self.PRT.searchitem(parsed_interest[1])
        if(index_number):
            # item is a string list like ['/ndn/ie/tcd/controller01/update/' '/kaikai/xinxin/' 'b' '1' '300']
            item = self.PRT.prefixtable[index_number]
            returndatacontent = str(item[2])      #item[2] is the origion
        else:
            returndatacontent = None
        print(returndatacontent)
        data = self.set_returndata(interest, returndatacontent)
        transport.send(data.wireEncode().toBuffer())


    def set_returndata(self, interest, returndatacontent):
        interestName = interest.getName()
        data = Data(interestName)
        data.setContent(returndatacontent)   #suppose the returndatacontent is string
        hourMilliseconds = 0  # here I should set it 0 since it always need to fresh.
        data.getMetaInfo().setFreshnessPeriod(hourMilliseconds)
        self.keyChain.sign(data, self.keyChain.getDefaultCertificateName())
        return(data)



    #this is just for original example.
    def onInterest(self, mainPrefix, interest, transport, registeredPrefixId):
        print("--------received interest:" + interest.getName().toUri())  #for test
        interestName = interest.getName()

        data = Data(interestName)
        data.setContent("<<< " + interestName.toUri() + '>>>>\n' + '<<<<'+ '--->>>' )

        hourMilliseconds = 0   # here I should set it 0 since it always need to fresh.
        data.getMetaInfo().setFreshnessPeriod(hourMilliseconds)

        self.keyChain.sign(data, self.keyChain.getDefaultCertificateName())
        transport.send(data.wireEncode().toBuffer())
        print("Replied to: %s" % interestName.toUri())

    def onRegisterFailed(self, mainPrefix):
        print("Register failed for prefix", mainPrefix.toUri())
        self.isDone = True


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Parse command line args for ndn producer')
    # #parser.add_argument("-n", "--namespace", required=True, help='namespace to listen under')
    #
    # args = parser.parse_args()

    try:
        #namespace = args.namespace
        Producer().run()

    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)