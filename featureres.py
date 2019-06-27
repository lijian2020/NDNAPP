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

import sys
import time
import argparse
import traceback


from pyndn import Name
from pyndn import Face
from pyndn.security import KeyChain
from oscommand import OSCommand
from ndnflowtable import NdnFlowTable
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
        feature_msg_prefix = Name('/ndn/{}-site/{}/ofndn/feature'.format(self.nodeid, self.nodeid))
        self.face.setInterestFilter(feature_msg_prefix, self.onInterest_Feature)  # for FeatureReq

        packetout_msg_prefix = Name('/ndn/{}-site/{}/ofndn/--/n1.0/13/0/0'.format(self.nodeid, self.nodeid))
        self.face.setInterestFilter(packetout_msg_prefix, self.onInterest_PacketOut)  # for PacketOut msg

        facemod_msg_prefix = Name('/ndn/{}-site/{}/ofndn/--/n1.0/16/0/0'.format(self.nodeid, self.nodeid))
        self.face.setInterestFilter(facemod_msg_prefix, self.onInterest_FaceMod)  # for FaceMod msg


        print(NodePrefix.toUri())


        # # Run the event loop forever. Use a short sleep to
        # # prevent the Producer from using 100% of the CPU.
        # while not self.isDone:
        #     self.face.processEvents()
        #     time.sleep(0.01)
        countnumber = 0
        while countnumber < 20000:
            self.face.processEvents()
            time.sleep(0.01)
            countnumber += 1
        # print("10s feature response listening stop")



    def onInterest_PacketOut(self, mainPrefix, interest, transport, registeredPrefixId):
        print("--------Received <<<PacketOut>>> interest Msg" )
        PacketOut_suffix = NdnFlowTable.parse_PacketOut_Interest(interest)
        NdnFlowTable.derectly_updatendnflowtable(PacketOut_suffix,self.nodeid)
        print("--------Updated the NdnFlowTable")
        self.isDone = True  #

    def onInterest_FaceMod(self, mainPrefix, interest, transport, registeredPrefixId):
        print("--------Received <<<FaceMod>>> interest Msg" )
        FaceMod_suffix_list = NdnFlowTable.parse_FaceMod_Interest(interest)
        # FaceMod_suffix_list pattern:[faceid, action]

        print(OSCommand.facemod(FaceMod_suffix_list))  # modify the face and print the command output
        self.isDone = True  #



    def onInterest_Feature(self, mainPrefix, interest, transport, registeredPrefixId):
        print("--------Received <<<FeatureReq>>> interest Msg")

        feature_face = OSCommand.getface()
        feature_FIB = OSCommand.getFIB()
        nodeid = bytes(self.nodeid,'utf-8')

        feature_data =nodeid + b'----' + feature_face + b'----' + feature_FIB

        data = OFMSG().create_feature_res_data(interest,feature_data)

        transport.send(data.wireEncode().toBuffer())
        print("--------Sent <<<FeatureRes>>> Data Msg")
        self.isDone = True  #

    def onInterest_Mian(self, mainPrefix, interest, transport, registeredPrefixId):
        pass
        #print("--------received Main interest:" + interest.getName().toUri())


    def onRegisterFailed(self, ControllerPrefix):
        print("Register failed for prefix", ControllerPrefix.toUri())
        self.isDone = True





