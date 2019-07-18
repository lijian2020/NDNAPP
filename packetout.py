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

'''This module is used to send PacketOut message. It also handles the return data'''

import time
from pyndn import Face
from pyndn.security import KeyChain
from ofmsg import OFMSG

class PacketOutMsg(object):
    '''FlowRemoved message is an interest send once, no need response '''

    def __init__(self):
        self.keyChain = KeyChain()
        self.ofmsg = OFMSG()
        self.face = Face()

    def run(self,PacketOut_suffix):
        try:
            self._sendPacketOutInterest(PacketOut_suffix)
            n=0
            while n<200:
                self.face.processEvents()
                time.sleep(0.01)
                n+=1
        except RuntimeError as e:
            print("ERROR: %s" %  e)
        return True

    def _sendPacketOutInterest(self,PacketOut_suffix):
        interest = self.ofmsg.create_packetout_msg_interest(PacketOut_suffix)
        uri = interest.getName().toUri()
        self.face.expressInterest(interest, self._onData, self._onTimeout)
        print("--------Sent <<<PacketOut>>> Interest ---------")


    def _onData(self, interest, data):
        pass
    def _onTimeout(self, interest):
        pass


if __name__ == '__main__':
    PacketOutMsg().run()

