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

'''This module is the OF-SDN 'client', which needs to be run on every NDN node.
Before running this code, the OF-SDN controller side should be run first, so that
this node could report to the controller.
---This module used multiple threads to handle different tasks.
---This module included some other functions, refer to its optional arguments
'''

import sys
import time
import argparse
import traceback
import subprocess


from pyndn import Face
from oscommand import OSCommand
from helloreq import HelloReq
from status.status_monitor import Status_Monitor
from flowremoved import FlowRemovedMsg
from packetin import PacketIn
from featureres import FeatureRes
from ctrlinforeq import CtrlInfoReq
from threading import Thread
from errormsg import ErrorMsg
from of_route_processor import OF_Route_Processor

class Node(object):

    def __init__(self):
        self.outstanding = dict()  #a dictionary to keep track of outstanding Interests and retransmissions.
        self.isDone = False
        #self.face = Face("127.0.0.1")
        self.face = Face()
        self.nodeid = OSCommand.getnodeid()

    def run(self, packetin=False, fr=False, error=False):
        #advertise a prefix for offering feature request
        NodePrefixString = '/ndn/{}-site/{}/ofndn'.format(self.nodeid,self.nodeid)
        subprocess.call(["export HOME=/tmp/minindn/{0} && nlsrc advertise {1} ".\
                                        format(self.nodeid,NodePrefixString)],shell=True)

        ########   Basic function  #######

        hello_threed = Thread(target=self.Hellorequest)  # send helloreq
        hello_threed.start()

        ctrlinfo_threed = Thread(target=self._sendCtrlInfoReqMsg)  # send ctrlinfo
        ctrlinfo_threed.start()

        feature_threed = Thread(target=self.Feature_service)  # send reature_data
        feature_threed.start()

        of_route_threed = Thread(target=self.OF_Route)  # listen noNextHop log and send packetin
        of_route_threed.start()



        ########   Advanced function  #######
        time.sleep(15)
        '''This section is used to send packetin msg if necessary'''
        unknown_prefix = "/abcd/dfgh/tcd"
        if(packetin):
            prefixinquire_threed = Thread(target=self.prefixinquire,args=(unknown_prefix,))
            prefixinquire_threed.start()

        '''This section is used to send flowremoved msg if necessary'''
        removed_prefix = "/abcd/dfgh/tcd"
        if (fr):
            flowremoved_threed = Thread(target=self._sendFlowRemovedMsg, args=(removed_prefix,))
            flowremoved_threed.start()

        '''This section is used to send error msg if necessary'''
        error_prefix = "{}--0x0004--0x0000--faceid255-down".format(self.nodeid)
        if (error):
            time.sleep(7)
            errormsg_threed = Thread(target=self._errormsg, args=(error_prefix,))
            errormsg_threed.start()





    def Hellorequest(self):
        Status_Monitor().run()

    def Feature_service(self):
        FeatureRes().run()

    def OF_Route(self):
        time.sleep(8)
        OF_Route_Processor().loglistener()

    def prefixinquire(self,unknown_prefix):
        if(PacketIn().run(unknown_prefix)):
            print("NDN FlowTable has been updated")

    def _errormsg(self, error_prefix):
        ErrorMsg().run(error_prefix)


    def _sendFlowRemovedMsg(self,removed_prefix):
        FlowRemovedMsg().run(removed_prefix)

    def _sendCtrlInfoReqMsg(self):
        time.sleep(5)
        CtrlInfoReq().run()  # here need other thread.




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse command line args for ndn consumer')
    parser.add_argument("-p", "--packetin", nargs='?', const=True, help='True | False send PacketIn msg?')
    parser.add_argument("-fr", "--flowremoved", nargs='?', const=True, help='True | False send FlowRemoved msg?')
    parser.add_argument("-e", "--error", nargs='?', const=True, help='True | False send Error msg?')
    args = parser.parse_args()

    try:
        packetin = args.packetin
        fr = args.flowremoved
        error = args.error
        Node().run(packetin, fr, error)

    except:
        traceback.print_exc(file=sys.stdout)
        print("Error parsing command line arguments")
        sys.exit(1)