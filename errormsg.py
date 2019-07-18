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

'''This module is used to send Error message. '''

import time
from pyndn import Interest
from pyndn import Face
from pyndn.security import KeyChain
from oscommand import OSCommand
from ofmsg import OFMSG
from ndnflowtable import NdnFlowTable


class ErrorMsg(object):
    '''Error report message is an interest for report error to controller'''

    def __init__(self):
        self.keyChain = KeyChain()
        self.isDone = False
        self.ofmsg = OFMSG()
        self.outstanding = dict()  # a dictionary to keep track of outstanding Interests and retransmissions.
        # self.face = Face("127.0.0.1")
        self.face = Face()
        self.nodeid = OSCommand.getnodeid()

    def run(self, unknown_prefix="h1--0x0004--0x0000--faceid255-down"):
        try:
            self._sendErrorMsgInterest(unknown_prefix)

            while not self.isDone:
                self.face.processEvents()
                time.sleep(0.01)
        except RuntimeError as e:
            print("ERROR: %s" % e)
        return self.isDone

    def _sendErrorMsgInterest(self, error_prefix):
        interest = self.ofmsg.create_error_msg_interest(error_prefix)
        uri = interest.getName().toUri()

        if uri not in self.outstanding:
            self.outstanding[uri] = 1
        self.face.expressInterest(interest, self._onData, self._onTimeout)
        print("--------Sent <<<Error Msg>>> Interest for \n %s" % uri)

    def _onData(self, interest, data):
        payload = data.getContent()
        name = data.getName()
        print("Received <<<<Error Msg ACK>>>>from Controller ")

        del self.outstanding[name.toUri()]
        self.isDone = True

    def _onTimeout(self, interest):
        name = interest.getName()
        uri = name.toUri()

        print("TIMEOUT #%d: %s" % (self.outstanding[uri], uri))
        self.outstanding[uri] += 1

        if self.outstanding[uri] <= 3:
            self.run()
        else:
            self.isDone = True


if __name__ == '__main__':
    ErrorMsg().run()
