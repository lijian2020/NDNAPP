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
from ctrlinfo_operation import CtrlInfo_Operation


class CtrlInfoReq(object):
    '''Request Control information '''

    def __init__(self):
        self.keyChain = KeyChain()
        self.isDone = False
        self.ofmsg = OFMSG()
        self.outstanding = dict()  # a dictionary to keep track of outstanding Interests and retransmissions.
        # self.face = Face("127.0.0.1")
        self.face = Face()
        self.nodeid = OSCommand.getnodeid()
        self.send_ctrlinfo_interest = True
        self.ctrlinfo_operation = CtrlInfo_Operation()

    def run(self):
        ctrlinfo_version_number = 100001
        while True:
            if (self.send_ctrlinfo_interest):
                try:
                    self._sendCtrlInfoInterest(ctrlinfo_version_number)
                    ctrlinfo_version_number += 1
                    self.send_ctrlinfo_interest = False  # repeat to send this interest.
                    self.isDone = False

                    while not self.isDone:
                        self.face.processEvents()
                        time.sleep(0.01)
                except RuntimeError as e:
                    print("ERROR: %s" % e)

            time.sleep(0.1)


    def _sendCtrlInfoInterest(self, ctrlinfo_version_number=100001):
        interest = self.ofmsg.create_ctrlinfo_req_interest(self.nodeid, ctrlinfo_version_number)
        uri = interest.getName().toUri()

        if uri not in self.outstanding:
            self.outstanding[uri] = 1
        self.face.expressInterest(interest, self._onData, self._onTimeout)
        print("******** Sent <<<CtrlInfoReq>>> Interest ******** \n {0} \n".format(uri))

    def _onData(self, interest, data):
        payload = data.getContent()
        name = data.getName()
        print("Received New <<<Control Information>>>------- \n", payload.toRawStr())
        del self.outstanding[name.toUri()]
        self.isDone = True
        self.send_ctrlinfo_interest = True
        self.ctrlinfo_operation.run(payload)



    def _onTimeout(self, interest):
        name = interest.getName()
        uri = name.toUri()

        print("TIMEOUT #%d: %s" % (self.outstanding[uri], uri))
        self.outstanding[uri] += 1

        if self.outstanding[uri] <= 3:
            self._sendCtrlInfoInterest()
        else:
            self.isDone = True


if __name__ == '__main__':
    CtrlInfoReq().run()
