import os
import time
import datetime
import pyinotify
import logging
from packetin import PacketIn
from oscommand import OSCommand
from ndnflowtable import NdnFlowTable


class OF_Route_Processor():
    '''This class process the case that NDN node has no next hop.
    It is a trigger that invokes the open flow procedure to search
    the local openflow table and send packet-in message to controller'''

    def __init__(self):
        self.nodeid = OSCommand.getnodeid()
        self.unknownprefixtable = set()

    def loglistener(self):
        '''this method listens the file '/tmp/mininet/node_id/nfd.log',
        if there is new log items indecate 'noNextHop', this method
        will deal with it'''

        pos = 0
        log_file = r'/tmp/minindn/{}/nfd.log'.format(self.nodeid, self.nodeid)
        print('==========2222============')
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
