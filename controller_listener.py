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
from ndnflowtable import NdnFlowTable



class Controller_Listener(object):
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


    def run(self):

        ControllerPrefixString = '/ndn/ie/tcd/controller01/ofndn/'
        ControllerPrefix = Name(ControllerPrefixString)
        self.face.setCommandSigningInfo(self.keyChain, \
                                   self.keyChain.getDefaultCertificateName())

        self.face.registerPrefix(ControllerPrefix, self.onInterest_Mian, self.onRegisterFailed)  # run prefix

        #filters:
        # hello_msg_prefix = Name('/ndn/ie/tcd/controller01/ofndn/--/n1.0/0/0/0/')
        # self.face.setInterestFilter(hello_msg_prefix,self.onInterest_Hello)   #for HelloReq msg

        error_msg_prefix = Name('/ndn/ie/tcd/controller01/ofndn/--/n1.0/1/0/0/')
        self.face.setInterestFilter(error_msg_prefix, self.onInterest_ErrorMsg)  # for Error msg

        packetin_msg_prefix = Name('/ndn/ie/tcd/controller01/ofndn/--/n1.0/10/0/0/')
        self.face.setInterestFilter(packetin_msg_prefix,self.onInterest_PacketIn)   #for packetin msg

        FlowRemoved_msg_prefix = Name('/ndn/ie/tcd/controller01/ofndn/--/n1.0/11/0/0/')
        self.face.setInterestFilter(FlowRemoved_msg_prefix,self.onInterest_FlowRemoved)   #for FlowRemoved msg

        # cannot be here, conflict with helloreq, since both of them occupy the 'listening channel' and will not release.
        # CtrlInfo_msg_prefix = Name('/ndn/ie/tcd/controller01/ofndn/--/n1.0/36/0/0/')
        # self.face.setInterestFilter(CtrlInfo_msg_prefix, self.onInterest_CtrlInfo)

        # Run the event loop forever. Use a short sleep to
        # prevent the Producer from using 100% of the CPU.
        while not self.isDone:             #listen hello cannot stop
            self.face.processEvents()
            time.sleep(0.01)

    def ctrl_info_run(self):

        ControllerPrefixString = '/ndn/ie/tcd/controller01/ofndn/'
        ControllerPrefix = Name(ControllerPrefixString)
        self.face.setCommandSigningInfo(self.keyChain, \
                                        self.keyChain.getDefaultCertificateName())

        self.face.registerPrefix(ControllerPrefix, self.onInterest_Mian, self.onRegisterFailed)  # run prefix

        # filters:
        CtrlInfo_msg_prefix = Name('/ndn/ie/tcd/controller01/ofndn/--/n1.0/36/0/0/')
        self.face.setInterestFilter(CtrlInfo_msg_prefix, self.onInterest_CtrlInfo)  # for CtrlInfo msg
        # Run the event loop forever. Use a short sleep to
        # prevent the Producer from using 100% of the CPU.
        while not self.isDone:  # listen hello cannot stop
            self.face.processEvents()
            time.sleep(0.01)




    def onInterest_PacketIn(self, mainPrefix, interest, transport, registeredPrefixId):
        print("------Received: <<<PacketIn>>> Msg for: \n" + interest.getName().toUri())  # for test
        unknown_prefix = NdnFlowTable.parse_Packetin_Interest(interest)

        # FlowModDataList: [ep(0),face(1),prefix(2),cookie(3),command(4),idle_timeout(5),
        # hard_timeout(6), priority(7),buffer_id(8),out_face(9),flag(10), action(11)]
        flowmod_data = '*---*---{}---None---0x0000---3600---36000\
        ---1---None---face=255---0x0001---0x0000'.format(unknown_prefix)
        data = self.ofmsg.create_flowmod_data(interest,flowmod_data)
        transport.send(data.wireEncode().toBuffer())

    def onInterest_FlowRemoved(self, mainPrefix, interest, transport, registeredPrefixId):

        print("------Received: <<<FlowRemoved>>> Msg ------")  # for test

    def onInterest_CtrlInfo(self, mainPrefix, interest, transport, registeredPrefixId):
        print("--------received <<<CtrlInfo Req>>> interest:\n" + interest.getName().toUri())  # for test
        while (self.new_CtrlInfo_data == self.CtrlInfo_data):  # wait for new data.
            time.sleep(5)
        self.CtrlInfo_data = self.new_CtrlInfo_data
        data = self.ofmsg.create_ctrlinfo_res_data(interest, self.CtrlInfo_data)
        transport.send(data.wireEncode().toBuffer())
        print("--------sent <<<New CtrlInfo Res>>> Data--------")

    def onInterest_Hello(self, mainPrefix, interest, transport, registeredPrefixId):
        print("--------received <<<HelloReq>>> interest:\n" + interest.getName().toUri())  # for test

        #todo(lijian) should check the helloreq_name_list and determine what action should do

        hello_data = 'this is the hello response data'
        data = self.ofmsg.create_hello_res_data(interest,hello_data)
        transport.send(data.wireEncode().toBuffer())
        NodePrefixTable.updatenodeprefixtable(interest)       #to add NPT and fetch feature

    def onInterest_ErrorMsg(self, mainPrefix, interest, transport, registeredPrefixId):
        print("--------received <<<Error Msg>>> interest:\n" + interest.getName().toUri())  # for test
        errormsg_data = 'Error Report Acknowledge'
        data = self.ofmsg.create_errorAck_data(interest, errormsg_data)
        transport.send(data.wireEncode().toBuffer())
        print("--------sent <<<Error Msg ACK>>>---------")

        # todo(errorMsg) maybe this msg can status some other actions.
        #parse the errorMsg interest to get error information.



    def onInterest_Mian(self, mainPrefix, interest, transport, registeredPrefixId):
        # TODO(onInterest_Mian): check what should do.
        pass

    def onRegisterFailed(self, ControllerPrefix):
        print("Register failed for prefix", ControllerPrefix.toUri())
        self.isDone = True





