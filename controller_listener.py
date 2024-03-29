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

'''There are several controller listener used for listening incoming packets.
This module is used to listen 'Error', 'PacketIn' and 'FlowRemoved' messages.
And it also replies some message.
'''


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
        print(
            "######### Received <<<PacketIn>>> Interest #########\n {0} \n".format(interest.getName().toUri()))

        (node_id, unknown_prefix) = NdnFlowTable.parse_Packetin_Interest(interest)
        node_id = node_id.strip('/')

        # FlowModDataList: [ep(0),face(1),prefix(2),cookie(3),command(4),idle_timeout(5),
        # hard_timeout(6), priority(7),buffer_id(8),out_face(9),flag(10), action(11)]
        flowmod_data = self.create_PacketIn_Data(node_id, unknown_prefix)
        data = self.ofmsg.create_flowmod_data(interest,flowmod_data)
        transport.send(data.wireEncode().toBuffer())
        print('===== Send [ FlowMod Msg ] to {0}====='.format(node_id))

    def create_PacketIn_Data(self, node_id, unknown_prefix):
        # This function is just used for demonstration to send exact flowmod message.

        if node_id == 'h1':
            data_tring = '*---*---{}---None---0x0000---3600---36000---1---None---267---0x0001---0x0000'.format(
                unknown_prefix)
        elif node_id == 'h2':
            data_tring = '*---*---{}---None---0x0000---3600---36000---1---None---271---0x0001---0x0000'.format(
                unknown_prefix)
        elif node_id == 'h3':
            data_tring = '*---*---{}---None---0x0000---3600---36000---1---None---269---0x0001---0x0000'.format(
                unknown_prefix)
        elif node_id == 'h4':
            data_tring = '*---*---{}---None---0x0000---3600---36000---1---None---271---0x0001---0x0000'.format(
                unknown_prefix)
        elif node_id == 'h5':
            data_tring = '*---*---{}---None---0x0000---3600---36000---1---None---276---0x0001---0x0000'.format(
                unknown_prefix)
        elif node_id == 'h6':
            data_tring = '*---*---{}---None---0x0000---3600---36000---1---None---261---0x0001---0x0000'.format(
                unknown_prefix)
        elif node_id == 'h7':
            data_tring = '*---*---{}---None---0x0000---3600---36000---1---None---260---0x0001---0x0000'.format(
                unknown_prefix)
        elif node_id == 'h8':
            data_tring = '*---*---{}---None---0x0000---3600---36000---1---None---260---0x0001---0x0000'.format(
                unknown_prefix)
        elif node_id == 'h9':
            data_tring = '*---*---{}---None---0x0000---3600---36000---1---None---261---0x0001---0x0000'.format(
                unknown_prefix)
        elif node_id == 'h10':
            data_tring = '*---*---{}---None---0x0000---3600---36000---1---None---255---0x0001---0x0000'.format(
                unknown_prefix)
        elif node_id == 'a':
            data_tring = '*---*---{}---None---0x0000---3600---36000---1---None---255---0x0001---0x0000'.format(
                unknown_prefix)
        elif node_id == 'b':
            data_tring = '*---*---{}---None---0x0000---3600---36000---1---None---255---0x0001---0x0000'.format(
                unknown_prefix)
        elif node_id == 'c':
            data_tring = '*---*---{}---None---0x0000---3600---36000---1---None---255---0x0001---0x0000'.format(
                unknown_prefix)
        elif node_id == 'd':
            data_tring = '*---*---{}---None---0x0000---3600---36000---1---None---255---0x0001---0x0000'.format(
                unknown_prefix)
        elif node_id == 'e':
            data_tring = '*---*---{}---None---0x0000---3600---36000---1---None---255---0x0001---0x0000'.format(
                unknown_prefix)
        elif node_id == 'f':
            data_tring = '*---*---{}---None---0x0000---3600---36000---1---None---255---0x0001---0x0000'.format(
                unknown_prefix)
        else:
            data_tring = '*---*---{}---None---0x0000---3600---36000---1---None---255---0x0001---0x0000'.format(
                unknown_prefix)
        return data_tring




    def onInterest_FlowRemoved(self, mainPrefix, interest, transport, registeredPrefixId):

        print("------Received: <<<FlowRemoved>>> Msg ------")  # for test

    def onInterest_CtrlInfo(self, mainPrefix, interest, transport, registeredPrefixId):
        print("******** Received <<<CtrlInfoReq>>> Interest ******** \n {0} \n".format(interest.getName().toUri()))
        while (self.new_CtrlInfo_data == self.CtrlInfo_data):  # wait for new data.
            time.sleep(5)
        self.CtrlInfo_data = self.new_CtrlInfo_data
        data = self.ofmsg.create_ctrlinfo_res_data(interest, self.CtrlInfo_data)
        transport.send(data.wireEncode().toBuffer())
        print("******** Sent <<<New CtrlInfo Res>>> Data ******** \n")

    def onInterest_Hello(self, mainPrefix, interest, transport, registeredPrefixId):
        print(
            "\n --------Received <<<HelloReq>>> Interest --------\n {0} \n".format(
                interest.getName().toUri()))  # for test
        print("--------Sent <<<HelloRes>>> Data -------- \n")
        hello_data = '[This is hello response data]'
        data = self.ofmsg.create_hello_res_data(interest,hello_data)
        transport.send(data.wireEncode().toBuffer())
        NodePrefixTable.updatenodeprefixtable(interest)       #to add NPT and fetch feature

    def onInterest_ErrorMsg(self, mainPrefix, interest, transport, registeredPrefixId):
        print("--------received <<<Error Msg>>> interest:\n" + interest.getName().toUri())  # for test
        errormsg_data = 'Error Report Acknowledge'
        data = self.ofmsg.create_errorAck_data(interest, errormsg_data)
        transport.send(data.wireEncode().toBuffer())
        print("--------sent <<<Error Msg ACK>>>---------")

        #parse the errorMsg interest to get error information.



    def onInterest_Mian(self, mainPrefix, interest, transport, registeredPrefixId):
        pass

    def onRegisterFailed(self, ControllerPrefix):
        print("Register failed for prefix", ControllerPrefix.toUri())
        self.isDone = True





