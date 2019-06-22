#!/usr/bin/python

# Copyright (c) 2013-2014 Regents of the University of California.
# Copyright (c) 2014 Susmit Shannigrahi, Steve DiBenedetto

# This file is part of ndn-cxx library (NDN C++ library with eXperimental eXtensions).
#
# ndn-cxx library is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# ndn-cxx library is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.
#
# You should have received copies of the GNU General Public License and GNU Lesser
# General Public License along with ndn-cxx, e.g., in COPYING.md file.  If not, see
# <http://www.gnu.org/licenses/>.
#
# See AUTHORS.md for complete list of ndn-cxx authors and contributors.
#
# @author Wentao Shang <http://irl.cs.ucla.edu/~wentao/>
# @author Steve DiBenedetto <http://www.cs.colostate.edu/~dibenede>
# @author Susmit Shannigrahi <http://www.cs.colostate.edu/~susmit>


import time
from pyndn import Interest
from pyndn import Face
from pyndn.security import KeyChain
from oscommand import OSCommand
from ofmsg import OFMSG
from ndnflowtable import NdnFlowTable


class PacketIn(object):
    '''PacketIn message is an interest for inquiring unknown prefix '''

    def __init__(self):
        self.keyChain = KeyChain()
        self.isDone = False
        self.ofmsg = OFMSG()
        self.outstanding = dict()  #a dictionary to keep track of outstanding Interests and retransmissions.
        #self.face = Face("127.0.0.1")
        self.face = Face()
        #self.nodeid = OSCommand.getnodeid()



    def run(self,unknown_prefix):
        try:
            self._sendPacketinInterest(unknown_prefix)

            while not self.isDone:
                self.face.processEvents()
                time.sleep(0.01)
        except RuntimeError as e:
            print("ERROR: %s" %  e)
        return self.isDone


    def _sendPacketinInterest(self,unknown_prefix):
        interest = self.ofmsg.create_packetin_msg_interest(unknown_prefix)
        uri = interest.getName().toUri()

        if uri not in self.outstanding:
            self.outstanding[uri] = 1
        self.face.expressInterest(interest, self._onData, self._onTimeout)

        print("Sent PacketIn Interest for %s" % uri)



    def _onData(self, interest, data):
        payload = data.getContent()
        name = data.getName()
        print("Received <<<<FlowMod data>>>>from Controller ")
        #todo(lijian)  add this item to flow table.
        self.nodeid = OSCommand.getnodeid()

        FlowModDataList = NdnFlowTable.parse_FlowMod_Data(payload)
        NdnFlowTable.updatendnflowtable(FlowModDataList,self.nodeid)
        print(NdnFlowTable)


        del self.outstanding[name.toUri()]
        self.isDone = True


    def _onTimeout(self, interest):
        name = interest.getName()
        uri = name.toUri()

        print("TIMEOUT #%d: %s" % (self.outstanding[uri], uri))
        self.outstanding[uri] += 1

        if self.outstanding[uri] <= 3:
            self._sendPacketinInterest()
        else:
            self.isDone = True




if __name__ == '__main__':
    PacketIn().run()

