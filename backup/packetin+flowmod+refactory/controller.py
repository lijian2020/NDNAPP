# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2014 Regents of the University of California.
# Copyright (c) 2014 Susmit Shannigrahi, Steve DiBenedetto
#
# Author: Jeff Thompson <jefft0@remap.ucla.edu>
# Author Steve DiBenedetto <http://www.cs.colostate.edu/~dibenede>
# Author Susmit Shannigrahi <http://www.cs.colostate.edu/~susmit>
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
from featurereq import FeatureReq
from multiprocessing import Process
from node_prefix_table import NodePrefixTable

class Controller(object):
    def __init__(self):
        self.keyChain = KeyChain()
        self.isDone = False
        self.ofmsg = OFMSG()
        self.nodeid = OSCommand.getnodeid()
        self.face = Face()# Create a connection to the local forwarder over a Unix socket
        self.outstanding = dict()  # a dictionary to keep track of outstanding Interests and retransmissions.
        self.hellores = Controller_Listener()
        self.featurereq = FeatureReq()
        #self.RLock = threading.RLock()





    def run(self):
        ControllerPrefixString = '/ndn/ie/tcd/controller01/ofndn/'
        subprocess.call(["export HOME=/tmp/minindn/{0} && nlsrc advertise {1} ". \
                        format(self.nodeid,ControllerPrefixString)],shell=True)

        self.hellores.run()  # other thread for hello msg



    def test(self):     #test
        for i in range(10):
            #self.RLock.acquire()
            time.sleep(5)
            print("=============before hellores=========")
            NPT = np.loadtxt('/tmp/minindn/NPT.txt',dtype=str)
            print(NPT)

            # Face_array = np.loadtxt(r'/tmp/minindn/Face_array.txt',dtype=str)
            # FIB_array = np.loadtxt(r'/tmp/minindn/FIB_array.txt',dtype=str)

            print("=============after hellores=========")
            #self.RLock.release()




if __name__ == '__main__':    ##### Multiprocess must start from here (__name__ = '__main__')

    # parser = argparse.ArgumentParser(description='Parse command line args for ndn producer')
    # #parser.add_argument("-n", "--namespace", required=True, help='namespace to listen under')
    # args = parser.parse_args()

    try:
        #namespace = args.namespace
        controller = Controller()
        t1 = Process(target=controller.run)
        t2 = Process(target=controller.test)    #put it before hello listen function.
        t1.start()
        time.sleep(20)
        t2.start()
    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)