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
import ofmsg
import random

from pyndn import Name
from pyndn import Data
from pyndn import Face
from pyndn.security import KeyChain
from oscommand import OSCommand
from ofmsg import OFMSG
from featurereq import FeatureReq
from controller_listener import Controller_Listener
from threading import Thread
from multiprocessing import Process

class Controller(object):
    def __init__(self):
        self.keyChain = KeyChain()
        self.isDone = False
        self.ofmsg = OFMSG()
        self.nodeid = OSCommand.getnodeid()
        self.face = Face()# Create a connection to the local forwarder over a Unix socket
        self.outstanding = dict()  # a dictionary to keep track of outstanding Interests and retransmissions.
        self.hello_req_name_list =[]
        self.hellores = Controller_Listener()
        self.hellores_thread=Process(target=self.hellores.run())  #other thread for hello msg
        self.hellores_thread.start()
        # self.controller_thread=Process(target=self.hello_msg_roundrobin())  #other thread for hello msg
        # self.controller_thread.start()




    "this is use another thread to monitoring_function a loop to send hello msg"
    def hello_msg_roundrobin(self):
        while True:
            self.run()
            time.sleep(4)




    def run(self):
        ControllerPrefixString = '/ndn/ie/tcd/controller01/ofndn/'
        subprocess.call(["export HOME=/tmp/minindn/{0} && nlsrc advertise {1} ". \
                        format(self.nodeid,ControllerPrefixString)],shell=True)
        print('llllllllllllllllllllllll')
        hello_req_name_list = self.hellores.helloreq_name_list
        print('<<<<<<<<===={}====>>>>>>>>>'.format(hello_req_name_list))





try:
    Controller().run()

except:
    traceback.print_exc(file=sys.stdout)
    sys.exit(1)
#


# if __name__ == '__main__':
#     # parser = argparse.ArgumentParser(description='Parse command line args for ndn producer')
#     # #parser.add_argument("-n", "--namespace", required=True, help='namespace to listen under')
#     #
#     # args = parser.parse_args()
#
#     try:
#         #namespace = args.namespace
#         Controller().monitoring_function()
#
#     except:
#         traceback.print_exc(file=sys.stdout)
#         sys.exit(1)