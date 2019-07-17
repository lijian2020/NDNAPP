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
import subprocess
from pyndn import Face
from pyndn.security import KeyChain
from oscommand import OSCommand
from ofmsg import OFMSG
from controller_listener import Controller_Listener
from controller_listener_ctrlinfo import Controller_Listener_CtrlInfo
from controller_listener_hello import Controller_Listener_Hello
from controller_setter import Controller_Setter
from featurereq import FeatureReq
from multiprocessing import Process
from threading import Thread


class Controller(object):
    def __init__(self):

        self.nodeid = OSCommand.getnodeid()
        self.controller_listener = Controller_Listener()
        self.controller_listener_ctrlinfo = Controller_Listener_CtrlInfo()
        self.controller_listener_hello = Controller_Listener_Hello()
        self.controller_setter = Controller_Setter()

    '''This hello function has to be imployment in a separated process, since it will
    conflict with other process if they are in the same thread/process'''

    def hello_function(self):
        ControllerPrefixString = '/ndn/ie/tcd/controller01/ofndn/'
        subprocess.call(["export HOME=/tmp/minindn/{0} && nlsrc advertise {1} ". \
                        format(self.nodeid,ControllerPrefixString)],shell=True)

        self.controller_listener_hello.hello_run()  # other thread for hello msg



    '''This ctrl_info function has to be imployment in a separated process, since it will
    conflict with other process if they are in the same thread/process'''

    def ctrl_info_function(self, ctrlinfo_parameter):  # a separated process for ctrl_info function
        if (ctrlinfo_parameter):
            self.controller_listener_ctrlinfo.new_CtrlInfo_data = '0x0001--0x0001--355'
            # facemod--destroy--faceid
        self.controller_listener_ctrlinfo.ctrl_info_run()

    # def ctrl_info_function(self):  # a separated process for ctrl_info function
    #     time.sleep(7)
    #     self.controller_listener.ctrl_info_run()

    def monitoring_function(self):
        self.controller_listener.run()  # other thread for error/packetin/flowremoved msg



    def control_function(self,functionlist):
        if 'packetout' in functionlist:
            self.controller_setter.packetoutsender()
        if 'facemod' in functionlist:
            self.controller_setter.facemodsender()



if __name__ == '__main__':    ##### Multiprocess must start from here (__name__ = '__main__')

    parser = argparse.ArgumentParser(description='Parse command line args for ndn producer')
    parser.add_argument("-p", "--packetout", nargs='?', const=True, help='True | False send PacketOut msg?')
    parser.add_argument("-f", "--facemod", nargs='?', const=True, help='True | False send FaceMod msg?')
    parser.add_argument("-c", "--ctrlinfo", nargs='?', const=True,
                        help='True | False test ctrlinfo response function?')
    args = parser.parse_args()

    try:
        #packetout = args.packetout
        controller = Controller()
        t1 = Process(target=controller.hello_function)  # a separated process for hello
        t1.start()

        t2 = Process(target=controller.ctrl_info_function,
                     args=(args.ctrlinfo,))  # a separated process for ctrl_info function
        t2.start()

        t3 = Process(target=controller.monitoring_function, )  # other thread for error/packetin/flowremoved msg
        t3.start()


        time.sleep(10)
        functionlist = []
        if(args.packetout):
            functionlist.append("packetout")
        if(args.facemod):
            functionlist.append("facemod")

        t4 = Process(target=controller.control_function, args=(functionlist,))
        t4.start()

    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)