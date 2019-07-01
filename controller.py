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
import subprocess
import numpy as np
from pyndn import Face
from pyndn.security import KeyChain
from oscommand import OSCommand
from ofmsg import OFMSG
from controller_listener import Controller_Listener
from controller_setter import Controller_Setter
from featurereq import FeatureReq
from multiprocessing import Process
from threading import Thread


class Controller(object):
    def __init__(self):
        #self.keyChain = KeyChain()
        #self.isDone = False
        #self.ofmsg = OFMSG()
        self.nodeid = OSCommand.getnodeid()
        #self.face = Face()# Create a connection to the local forwarder over a Unix socket
        #self.outstanding = dict()  # a dictionary to keep track of outstanding Interests and retransmissions.
        self.controller_listener = Controller_Listener()
        self.controller_setter = Controller_Setter()
        #self.featurereq = FeatureReq()
        #self.RLock = threading.RLock()




    def monitoring_function(self):
        ControllerPrefixString = '/ndn/ie/tcd/controller01/ofndn/'
        subprocess.call(["export HOME=/tmp/minindn/{0} && nlsrc advertise {1} ". \
                        format(self.nodeid,ControllerPrefixString)],shell=True)

        self.controller_listener.run()  # other thread for hello msg

    '''This ctrl_info function has to be imployment in a separated process, since it will
    conflict with hello process it they are in the same thread/process'''

    def ctrl_info_function(self, ctrlinfo_parameter):  # a separated process for ctrl_info function
        if (ctrlinfo_parameter):
            self.controller_listener.new_CtrlInfo_data = '0x0001--0x0001--255'
            # facemod--destroy--faceid
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
        self.controller_listener.ctrl_info_run()


    def control_function(self,functionlist):
        if 'packetout' in functionlist:
            self.controller_setter.packetoutsender()
        if 'facemod' in functionlist:
            self.controller_setter.facemodsender()



if __name__ == '__main__':    ##### Multiprocess must start from here (__name__ = '__main__')

    parser = argparse.ArgumentParser(description='Parse command line args for ndn producer')
    parser.add_argument("-p", "--packetout", nargs='?', const=True, help='True | False send PacketOut msg?')
    parser.add_argument("-f", "--facemod", nargs='?', const=True, help='True | False send FaceMod msg?') #todo(facemod)May need more arguments
    parser.add_argument("-c", "--ctrlinfo", nargs='?', const=True,
                        help='True | False test ctrlinfo response function?')  # todo(ctrlinfo)May need more arguments
    args = parser.parse_args()

    try:
        #packetout = args.packetout
        controller = Controller()
        t1 = Process(target=controller.monitoring_function)
        t1.start()

        t2 = Process(target=controller.ctrl_info_function,
                     args=(args.ctrlinfo,))  # a separated process for ctrl_info function
        t2.start()


        time.sleep(10)
        functionlist = []
        if(args.packetout):
            functionlist.append("packetout")
        if(args.facemod):
            functionlist.append("facemod")

        t3 = Process(target=controller.control_function, args=(functionlist,))
        t3.start()

    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)