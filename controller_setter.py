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

'''This module is used for some specific functions or tests for  controller. '''

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
from packetout import PacketOutMsg
from facemod import FaceModMsg
from node_prefix_table import NodePrefixTable



class Controller_Setter(object):
    def __init__(self):
        pass
        #self.keyChain = KeyChain()
        #self.isDone = False
        #self.ofmsg = OFMSG()
        #self.nodeid = OSCommand.getnodeid()
        #self.face = Face()
        #self.featurereq = FeatureReq()
        #self.helloreq_name_list = []


    def run(self):
        pass


    def packetoutsender(self):
        '''This section is used to send packetout msg if necessary'''
        PacketOut_suffix = "all---all---/Ireland/Dublin/TCD/---2---0---3600---36000---0x0001---faceid255---0x0001"
        PacketOutMsg().run(PacketOut_suffix)

    def facemodsender(self):
        '''This section is used to send facemod msg if necessary'''
        facemod_suffix = "255---0x0001"  # "faceid---Action"; Action ={create=0x0000, destroy=0x0001}
        FaceModMsg().run(facemod_suffix)