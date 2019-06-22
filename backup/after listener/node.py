#!/usr/bin/python

# Copyright (c) 2013-2014 Regents of the University of California.
# Copyright (c) 2014 Susmit Shannigrahi, Steve DiBenedetto

# This file is part of ndn-cxx library (NDN C++ library with eXperimental eXtensions).
#
# ndn-cxx library is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# ndn-cxx library is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.
#
# You should have received copies of the GNU General Public License and GNU Lesser
# General Public License along with ndn-cxx, e.g., in COPYING.md file.  If not, see
# <http://www.gnu.org/licenses/>.
#
# See AUTHORS.md for complete list of ndn-cxx authors and contributors.
#
# @author Wentao Shang <http://irl.cs.ucla.edu/~wentao/>
# @author Steve DiBenedetto <http://www.cs.colostate.edu/~dibenede>
# @author Susmit Shannigrahi <http://www.cs.colostate.edu/~susmit>

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
from threading import Thread

class Node(object):
    '''Hello '''

    def __init__(self):
        self.outstanding = dict()  #a dictionary to keep track of outstanding Interests and retransmissions.
        self.isDone = False
        #self.face = Face("127.0.0.1")
        self.face = Face()
        self.nodeid = OSCommand.getnodeid()
        #self.featureres =FeatureRes()
        # self.helloreq_thread=Thread(target=self.hello_msg_roundrobin)  #other thread for hello msg
        # self.helloreq_thread.start()


    # "this is use another thread to monitoring_function a loop to send hello msg"
    # def hello_msg_roundrobin(self):
    #     while True:
    #         HelloReq().monitoring_function()
    #         time.sleep(4)


    def run(self,packetin=False,fr=False):
        #advertise a prefix for offering feature request
        NodePrefixString = '/ndn/{}-site/{}/ofndn'.format(self.nodeid,self.nodeid)
        subprocess.call(["export HOME=/tmp/minindn/{0} && nlsrc advertise {1} ".\
                                        format(self.nodeid,NodePrefixString)],shell=True)


        hello_threed = Thread(target=self.Hellorequest)
        hello_threed.start()

        time.sleep(3)
        '''This section is used to send packetin msg if necessary'''
        unknown_prefix = "/abcd/dfgh/tcd"
        if(packetin):
            prefixinquire_threed = Thread(target=self.prefixinquire,args=(unknown_prefix,))
            prefixinquire_threed.start()

        '''This section is used to send packetin msg if necessary'''
        removed_prefix = "/abcd/dfgh/tcd"
        if (fr):
            flowremoved_threed = Thread(target=self._sendFlowRemovedMsg, args=(removed_prefix,))
            flowremoved_threed.start()



    def Hellorequest(self):
        if(HelloReq().run()):
            FeatureRes().run()

    def prefixinquire(self,unknown_prefix):
        if(PacketIn().run(unknown_prefix)):
            print("NDN FlowTable has been updated")

    def _sendFlowRemovedMsg(self,removed_prefix):
        FlowRemovedMsg().run(removed_prefix)





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse command line args for ndn consumer')
    parser.add_argument("-p", "--packetin",nargs='?', const=True, help='True | False send PacketIn msg?')
    parser.add_argument("-fr", "--flowremoved", nargs='?', const=True, help='True | False send FlowRemoved msg?')
    args = parser.parse_args()

    try:
        packetin = args.packetin
        fr = args.flowremoved
        Node().run(packetin,fr)

    except:
        traceback.print_exc(file=sys.stdout)
        print("Error parsing command line arguments")
        sys.exit(1)