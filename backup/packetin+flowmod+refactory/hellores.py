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
import random
from pyndn import Name
from pyndn import Face
from pyndn.security import KeyChain
from oscommand import OSCommand
from ofmsg import OFMSG
from featurereq import FeatureReq
from node_prefix_table import NodePrefixTable



class HelloRes(object):
    def __init__(self):
        self.keyChain = KeyChain()
        self.isDone = False
        self.ofmsg = OFMSG()
        self.nodeid = OSCommand.getnodeid()
        self.face = Face()
        self.featurereq = FeatureReq()
        self.helloreq_name_list = []


    def run(self):

        ControllerPrefixString = '/ndn/ie/tcd/controller01/ofndn/'
        ControllerPrefix = Name(ControllerPrefixString)
        self.face.setCommandSigningInfo(self.keyChain, \
                                   self.keyChain.getDefaultCertificateName())

        self.face.registerPrefix(ControllerPrefix, self.onInterest_Mian, self.onRegisterFailed) #main prefix
        #print(ControllerPrefix.toUri())

        #filters:
        hello_msg_prefix = Name('/ndn/ie/tcd/controller01/ofndn/--/n1.0/0/0/0/')
        self.face.setInterestFilter(hello_msg_prefix,self.onInterest_Hello)   #for HelloReq

        packetin_msg_prefix = Name('/ndn/ie/tcd/controller01/ofndn/--/n1.0/10/0/0/')
        self.face.setInterestFilter(packetin_msg_prefix,self.onInterest_PacketIn)   #for HelloReq

        #print(NodePrefixTable.NPT)

        # Run the event loop forever. Use a short sleep to
        # prevent the Producer from using 100% of the CPU.
        while not self.isDone:             #listen hello cannot stop
            self.face.processEvents()
            time.sleep(0.01)
        # countnumber = 0
        # while countnumber < 600:
        #     self.face.processEvents()
        #     time.sleep(0.01)
        #     countnumber += 1



    def onInterest_PacketIn(self, mainPrefix, interest, transport, registeredPrefixId):
        print("--------received PacketIn interest:" + interest.getName().toUri())  # for test
        #print(self.NPT.node_prefix_table)

        rand = random.randint(0,10)
        #todo(flowmod): get data for FlowMod msg from Upper APP
        flowmod_data = '*---*---/Msc/TCD/node-{}/---None---0x0000---3600---36000\
        ---1---None---face=245---0x0001---0x0000'.format(str(rand))
        data = self.ofmsg.create_flowmod_data(interest,flowmod_data)
        transport.send(data.wireEncode().toBuffer())



    def onInterest_Hello(self, mainPrefix, interest, transport, registeredPrefixId):
        print("--------received interest:" + interest.getName().toUri())  # for test
        #print(self.NPT.node_prefix_table)

        #todo(lijian) should check the helloreq_name_list and determine what action should do

        hello_data = 'this is the hello response data'
        data = self.ofmsg.create_hello_res_data(interest,hello_data)
        transport.send(data.wireEncode().toBuffer())
        NodePrefixTable.updatenodeprefixtable(interest)       #to add NPT and fetch feature



    def onInterest_Mian(self, mainPrefix, interest, transport, registeredPrefixId):
        # TODO(lijian): check what should do.
        pass

    def onRegisterFailed(self, ControllerPrefix):
        print("Register failed for prefix", ControllerPrefix.toUri())
        self.isDone = True





