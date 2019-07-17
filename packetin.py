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
        self.nodeid = OSCommand.getnodeid()

    def run(self, unknown_prefix="/abcd/dfgh/tcd"):
        try:
            self._sendPacketinInterest(unknown_prefix)

            while not self.isDone:
                self.face.processEvents()
                time.sleep(0.01)
        except RuntimeError as e:
            print("ERROR: %s" %  e)
        return self.isDone


    def _sendPacketinInterest(self,unknown_prefix):
        interest = self.ofmsg.create_packetin_msg_interest(unknown_prefix, self.nodeid)
        uri = interest.getName().toUri()

        if uri not in self.outstanding:
            self.outstanding[uri] = 1
        self.face.expressInterest(interest, self._onData, self._onTimeout)
        print("######### Sent <<<PacketIn>>> Interest #########\n {0} \n".format(uri))



    def _onData(self, interest, data):
        payload = data.getContent()
        name = data.getName()
        print("Received <<<<FlowMod data>>>>from Controller ")

        self.nodeid = OSCommand.getnodeid()

        # add this item to flow table.
        FlowModDataList = NdnFlowTable.parse_FlowMod_Data(payload)
        # print(FlowModDataList)
        NdnFlowTable.updatendnflowtable(FlowModDataList,self.nodeid)
        print(NdnFlowTable)


        del self.outstanding[name.toUri()]
        self.isDone = True


    def _onTimeout(self, interest):
        name = interest.getName()
        uri = name.toUri()

        print("TIMEOUT #%d: %s" % (self.outstanding[uri], uri))
        self.outstanding[uri] += 1
        self.isDone = True
        # if self.outstanding[uri] <= 3:
        #     self.run()
        # else:
        #     self.isDone = True




if __name__ == '__main__':
    PacketIn().run()

