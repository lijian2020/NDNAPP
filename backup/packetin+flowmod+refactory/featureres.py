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


from pyndn import Name
from pyndn import Face
from pyndn.security import KeyChain
from oscommand import OSCommand
from ofmsg import OFMSG
from featurereq import FeatureReq


class FeatureRes(object):
    def __init__(self):
        self.keyChain = KeyChain()
        self.isDone = False
        self.nodeid = OSCommand.getnodeid()
        self.face = Face()
        self.featurereq = FeatureReq()

    def run(self):
        NodePrefixString = '/ndn/{}-site/{}/ofndn'.format(self.nodeid, self.nodeid)
        NodePrefix = Name(NodePrefixString)
        self.face.setCommandSigningInfo(self.keyChain, \
                                   self.keyChain.getDefaultCertificateName())
        #self.face.registerPrefix(NodePrefix, self.onInterest, self.onRegisterFailed) #main prefix

        self.face.registerPrefix(NodePrefix, self.onInterest_Mian, self.onRegisterFailed) #main prefix

        # filters:
        hello_msg_prefix = Name('/ndn/{}-site/{}/ofndn/feature'.format(self.nodeid, self.nodeid))
        self.face.setInterestFilter(hello_msg_prefix, self.onInterest)  # for HelloReq

        print(NodePrefix.toUri())


        # # Run the event loop forever. Use a short sleep to
        # # prevent the Producer from using 100% of the CPU.
        # while not self.isDone:
        #     self.face.processEvents()
        #     time.sleep(0.01)
        countnumber = 0
        while countnumber < 10000:
            self.face.processEvents()
            time.sleep(0.01)
            countnumber += 1
        # print("10s feature response listening stop")





    def onInterest(self, mainPrefix, interest, transport, registeredPrefixId):
        print("--------received interest:" + interest.getName().toUri())  # for test
        interestName = interest.getName()
        #
        # data = Data(interestName)
        # data.setContent("<<< ====this is the node-{}'s feature=====>>>".format(self.nodeid))
        #
        # hourMilliseconds = 0  # here I should set it 0 since it always need to fresh.
        # data.getMetaInfo().setFreshnessPeriod(hourMilliseconds)
        #
        # self.keyChain.sign(data, self.keyChain.getDefaultCertificateName())
        #
        feature_face = OSCommand.getface()
        feature_FIB = OSCommand.getFIB()
        nodeid = bytes(self.nodeid,'utf-8')

        feature_data =nodeid + b'----' + feature_face + b'----' + feature_FIB

        data = OFMSG().create_feature_res_data(interest,feature_data)

        transport.send(data.wireEncode().toBuffer())
        print("Replied to: %s" % interestName.toUri())
        self.isDone = True  #

    def onInterest_Mian(self, mainPrefix, interest, transport, registeredPrefixId):
        #print("main prefix pass===========")
        pass

    def onRegisterFailed(self, ControllerPrefix):
        print("Register failed for prefix", ControllerPrefix.toUri())
        self.isDone = True





