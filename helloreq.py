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


class HelloReq(object):
    '''Hello '''

    def __init__(self):
        self.keyChain = KeyChain()
        self.isDone = False
        self.ofmsg = OFMSG()
        self.outstanding = dict()  #a dictionary to keep track of outstanding Interests and retransmissions.
        #self.face = Face("127.0.0.1")
        self.face = Face()
        self.nodeid = OSCommand.getnodeid()

    def run(self, hello_version_number):
        try:
            self._sendHelloInterest(hello_version_number)

            while not self.isDone:
                self.face.processEvents()
                time.sleep(0.01)
        except RuntimeError as e:
            print("ERROR: %s" %  e)
        return self.isDone

    def _sendHelloInterest(self, hello_version_number=100001):
        interest = self.ofmsg.create_hello_req_interest(self.nodeid, hello_version_number)
        uri = interest.getName().toUri()

        if uri not in self.outstanding:
            self.outstanding[uri] = 1
        self.face.expressInterest(interest, self._onData, self._onTimeout)

        print("--------Sent <<<Helloreq>>> Interest -------- \n {0} \n".format(uri))



    def _onData(self, interest, data):
        payload = data.getContent()
        name = data.getName()
        print("--------Received <<<HelloRes>>> Data -------- \n {0} \n".format(payload.toRawStr()))
        del self.outstanding[name.toUri()]
        self.isDone = True


    def _onTimeout(self, interest):
        name = interest.getName()
        uri = name.toUri()

        print("TIMEOUT #%d: %s" % (self.outstanding[uri], uri))
        self.outstanding[uri] += 1

        if self.outstanding[uri] <= 3:
            self._sendHelloInterest()
        else:
            self.isDone = True




if __name__ == '__main__':
    HelloReq().run()

