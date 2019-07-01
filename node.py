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
import subprocess


from pyndn import Face
from oscommand import OSCommand
from helloreq import HelloReq
from flowremoved import FlowRemovedMsg
from packetin import PacketIn
from featureres import FeatureRes
from ctrlinforeq import CtrlInfoReq
from threading import Thread
from errormsg import ErrorMsg

class Node(object):
    '''Hello '''

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

        ########   Advanced function  #######
        time.sleep(3)
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
        if(HelloReq().run()):
            FeatureRes().run()


    def prefixinquire(self,unknown_prefix):
        if(PacketIn().run(unknown_prefix)):
            print("NDN FlowTable has been updated")

    def _errormsg(self, error_prefix):
        ErrorMsg().run(error_prefix)


    def _sendFlowRemovedMsg(self,removed_prefix):
        FlowRemovedMsg().run(removed_prefix)

    def _sendCtrlInfoReqMsg(self):
        time.sleep(10)
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