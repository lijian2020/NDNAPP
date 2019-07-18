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


'''This module is used to send FeatureReq message. It also handles the return data'''
import sys
import time
import argparse
import traceback

from pyndn import Face
from pyndn.security import KeyChain
from oscommand import OSCommand
from ofmsg import OFMSG
from featuredata import FeatureDate



class FeatureReq(object):
    def __init__(self):
        self.keyChain = KeyChain()
        self.isDone = False
        self.ofmsg = OFMSG()
        self.outstanding = dict()  # a dictionary to keep track of outstanding Interests and retransmissions.
        self.face = Face()
        self.nodeid = OSCommand.getnodeid()




    def run(self,original_hello_req_interest):
        try:
            self._sendFeatureInterest(original_hello_req_interest)

            while not self.isDone:
                self.face.processEvents()
                time.sleep(0.01)

        except RuntimeError as e:
            print("ERROR: %s" %  e)


    def _sendFeatureInterest(self,feature_req_interest_name):
        interest = self.ofmsg.create_feature_req_interest(feature_req_interest_name)
        uri = interest.getName().toUri()

        if uri not in self.outstanding:
            self.outstanding[uri] = 1
        self.face.expressInterest(interest, self._onFeatureData, self._onTimeout)

        print("++++++++ Sent <<<FeatureReq>>> Interest ++++++++ \n {0} \n".format(uri))




    def _onFeatureData(self, interest, data):

        # originalfeaturedata = data.getContent.toRawStr()
        # #originalfeaturedata.toRawStr()
        # name = data.getName()
        # self.featurerdata.monitoring_function(originalfeaturedata)
        # print("Received new featureData ----updating FIB & Face table")
        # #print("Received data: ", payload.toRawStr())
        #
        # del self.outstanding[name.toUri()]
        # self.isDone = True

        payload = data.getContent()
        contentx = payload.toRawStr()
        name = data.getName()
        print("++++++++ Received <<<FeatureRes>>> Data ++++++++ \n")
        FeatureDate.run(contentx)

        del self.outstanding[name.toUri()]
        self.isDone = True
        print('========FIB Database has been updated=======')
        print('========Face Database has been updated=======\n')



    def _onTimeout(self, interest):
        name = interest.getName()
        uri = name.toUri()

        print("TIMEOUT #%d: %s" % (self.outstanding[uri], uri))
        self.outstanding[uri] += 1

        if self.outstanding[uri] <= 3:
            self._sendFeatureInterest(interest)
        else:
            self.isDone = True





if __name__ == '__main__':
    FeatureReq().run()







