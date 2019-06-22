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

from pyndn import Interest
from pyndn import Name
from pyndn import Face
from pyndn import encoding
from pyndn.security import KeyChain
from pyndn.util.blob import Blob
from oscommand import OSCommand
from ofmsg import OFMSG
from helloreq import HelloReq
from featureres import FeatureRes
from threading import Thread

class Consumer(object):
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


    def run(self):
        #advertise a prefix for offering feature request
        NodePrefixString = '/ndn/{}-site/{}/ofndn'.format(self.nodeid,self.nodeid)
        subprocess.call(["export HOME=/tmp/minindn/{0} && nlsrc advertise {1} ".\
                                        format(self.nodeid,NodePrefixString)],shell=True)

        if(HelloReq().run()):
            FeatureRes().run()
        # HelloReq().monitoring_function()
        # feature_threed = Thread(target=FeatureRes().monitoring_function)
        # feature_threed.start()
        #





# try:
#     Node().monitoring_function()
#
# except:
#     traceback.print_exc(file=sys.stdout)
#     print("Error parsing command line arguments")
#     sys.exit(1)
#


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Parse command line args for ndn consumer')
    # parser.add_argument("-u", "--uri", required=True, help='ndn name to retrieve')
    # args = parser.parse_args()

    try:
        # uri = args.uri
        Consumer().run()

    except:
        traceback.print_exc(file=sys.stdout)
        print("Error parsing command line arguments")
        sys.exit(1)