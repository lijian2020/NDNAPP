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
from pyndn import Face
from pyndn.security import KeyChain
from ofmsg import OFMSG

class FlowRemovedMsg(object):
    '''FlowRemoved message is an interest send once, no need response '''

    def __init__(self):
        self.keyChain = KeyChain()
        self.ofmsg = OFMSG()
        self.face = Face()

    def run(self,removed_prefix):
        try:
            self._sendFlowRemovedInterest(removed_prefix)
            n=0
            while n<200:
                self.face.processEvents()
                time.sleep(0.01)
                n+=1
        except RuntimeError as e:
            print("ERROR: %s" %  e)
        return True

    def _sendFlowRemovedInterest(self,removed_prefix):
        interest = self.ofmsg.create_flowremoved_msg_interest(removed_prefix)
        uri = interest.getName().toUri()
        self.face.expressInterest(interest, self._onData, self._onTimeout)
        print("--------Sent <<<FlowRemoved>>> Msg for %s" % uri)

    def _onData(self, interest, data):
        pass
    def _onTimeout(self, interest):
        pass


if __name__ == '__main__':
    FlowRemovedMsg().run()

