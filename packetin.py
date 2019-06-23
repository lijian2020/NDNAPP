#!/usr/bin/python
#
# Copyright (C) 2019 Regents of the Trinity College of Dublin, the University of Dublin.
# Copyright (c) 2019 Susmit Li Jian
#
# Author: Li Jian <lij12@tcd.ie>
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
#


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

        print("--------Sent <<<PacketIn>>> Interest for \n %s" % uri)



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

