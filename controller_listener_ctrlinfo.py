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


class Controller_Listener_CtrlInfo(object):
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

    def ctrl_info_run(self):

        ControllerPrefixString = '/ndn/ie/tcd/controller01/ofndn/--/n1.0/36/0/0/'
        ControllerPrefix = Name(ControllerPrefixString)
        self.face.setCommandSigningInfo(self.keyChain, \
                                        self.keyChain.getDefaultCertificateName())

        self.face.registerPrefix(ControllerPrefix, self.onInterest_CtrlInfo, self.onRegisterFailed)  # run prefix
        #
        # # filters:
        # CtrlInfo_msg_prefix = Name('/ndn/ie/tcd/controller01/ofndn/--/n1.0/36/0/0/')
        # self.face.setInterestFilter(CtrlInfo_msg_prefix, self.onInterest_CtrlInfo)  # for CtrlInfo msg

        # Run the event loop forever. Use a short sleep to
        # prevent the Producer from using 100% of the CPU.
        while not self.isDone:  # listen hello cannot stop
            self.face.processEvents()
            time.sleep(0.01)

    def onInterest_CtrlInfo(self, mainPrefix, interest, transport, registeredPrefixId):
        print("******** Received <<<CtrlInfoReq>>> Interest ******** \n {0} \n".format(interest.getName().toUri()))
        while (self.new_CtrlInfo_data == self.CtrlInfo_data):  # wait for new data.
            time.sleep(15)
        self.CtrlInfo_data = self.new_CtrlInfo_data
        data = self.ofmsg.create_ctrlinfo_res_data(interest, self.CtrlInfo_data)
        transport.send(data.wireEncode().toBuffer())
        print("******** Sent <<<New CtrlInfo Res>>> Data ******** \n")

    def onInterest_Mian(self, mainPrefix, interest, transport, registeredPrefixId):
        pass

    def onRegisterFailed(self, ControllerPrefix):
        print("Register failed for prefix", ControllerPrefix.toUri())
        self.isDone = True
