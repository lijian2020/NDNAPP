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