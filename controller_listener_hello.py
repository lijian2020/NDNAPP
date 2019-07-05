#!/usr/bin/python
#
# Copyright (C) 2019 Regents of the Trinity College of Dublin, the University of Dublin.
# Copyright (c) 2019 Submit Li Jian
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


class Controller_Listener_Hello(object):
    def __init__(self):
        self.keyChain = KeyChain()
        self.isDone = False
        self.ofmsg = OFMSG()
        self.nodeid = OSCommand.getnodeid()
        self.face = Face()
        self.featurereq = FeatureReq()
        self.helloreq_name_list = []
        self.new_CtrlInfo_data = "---Initial CtrlInfo data---"  # used to get new ctrlinfo data and send to nodes.
        self.CtrlInfo_data = ""  # used to record used ctrlinfo data

    def hello_run(self):
        ControllerPrefixString = '/ndn/ie/tcd/controller01/ofndn/--/n1.0/0/0/0/'
        ControllerPrefix = Name(ControllerPrefixString)
        self.face.setCommandSigningInfo(self.keyChain, \
                                        self.keyChain.getDefaultCertificateName())

        self.face.registerPrefix(ControllerPrefix, self.onInterest_Hello, self.onRegisterFailed)  # run prefix

        # Run the event loop forever. Use a short sleep to
        # prevent the Producer from using 100% of the CPU.
        while not self.isDone:  # listen hello cannot stop
            self.face.processEvents()
            time.sleep(0.01)

    def onInterest_Hello(self, mainPrefix, interest, transport, registeredPrefixId):
        print("--------received <<<HelloReq>>> interest:\n" + interest.getName().toUri())  # for test

        # todo(lijian) should check the helloreq_name_list and determine what action should do

        hello_data = 'this is the hello response data'
        data = self.ofmsg.create_hello_res_data(interest, hello_data)
        transport.send(data.wireEncode().toBuffer())
        NodePrefixTable.updatenodeprefixtable(interest)  # to add NPT and fetch feature

    def onInterest_Mian(self, mainPrefix, interest, transport, registeredPrefixId):
        # TODO(onInterest_Mian): check what should do.
        pass

    def onRegisterFailed(self, ControllerPrefix):
        print("Register failed for prefix", ControllerPrefix.toUri())
        self.isDone = True
