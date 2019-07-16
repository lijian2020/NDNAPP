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

