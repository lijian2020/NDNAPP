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

    def loglistener(self):
        '''this method listens the file '/tmp/mininet/node_id/nfd.log',
        if there is new log items indecate 'noNextHop', this method
        will deal with it'''

        pos = 0
        log_file = r'/tmp/minindn/{}-site/{}/nfd.log'.format(self.nodeid, self.nodeid)
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
                print('========={}======='.format(prefix))
                if (self.search_NFT(prefix)):
                    pass  # todo add item to rib
                else:
                    self.packetin_sender(prefix)
        except:
            print('there is no linelist[5]')

    def search_NFT(self, prefix):
        return True
        pass

    def packetin_sender(self, prefix):
        pass



if __name__ == '__main__':
    OF_Route_Processor().loglistener()
