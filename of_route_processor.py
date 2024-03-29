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

'''This class process the case that NDN node has no next hop.
    It is a trigger that invokes the open flow procedure to search
    the local openflow table and send packet-in message to controller'''

import os
import time
import datetime
import pyinotify
import logging
from packetin import PacketIn
from oscommand import OSCommand
from ndnflowtable import NdnFlowTable


class OF_Route_Processor():

    def __init__(self):
        self.nodeid = OSCommand.getnodeid()
        self.unknownprefixtable = set()

    def loglistener(self):
        '''this method listens the file '/tmp/mininet/node_id/nfd.log',
        if there is new log items indecate 'noNextHop', this method
        will deal with it'''

        pos = 0
        log_file = r'/tmp/minindn/{}/nfd.log'.format(self.nodeid, self.nodeid)
        while True:
            try:
                with open(log_file) as f:
                    if pos != 0:
                        f.seek(pos, 0)
                    while True:
                        line = f.readline()
                        if line.strip():
                            # print(line.strip())
                            linestr = line.strip()
                            self.noNextHopItems_log_checker(linestr)

                        pos = pos + len(line)
                        if not line.strip():
                            break
            except:
                print('error in open log file')

    def noNextHopItems_log_checker(self, linestr):
        '''select out the log items which include 'noNextHop' mark'''
        linelist = linestr.split()
        try:
            if (linelist[5] == 'noNextHop'):
                prefix = (linelist[3].split('?'))[0]
                if (not (prefix.startswith('/localhop/') \
                         or prefix.startswith('/ndn/ie/tcd/controller01/ofndn') \
                         or prefix.startswith('/ndn/{}-site/{}/ofndn'.format(self.nodeid, self.nodeid)) \
                         or prefix in self.unknownprefixtable)):
                    self.unknownprefixtable.add(prefix)
                    print('[No Route in RIB ] for \n {}'.format(prefix))
                    if (not NdnFlowTable.searchitem(prefix)):
                        PacketIn().run(prefix)
        except:
            pass

    # def packetin_sender(self, unknown_prefix):
    #     if (PacketIn().run(unknown_prefix)):
    #         print("NDN FlowTable has been updated")

#
#
# if __name__ == '__main__':
#     OF_Route_Processor().loglistener()
