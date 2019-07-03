
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

        print("Sent Interest for %s" % uri)



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
        #print("Received data========: \n", type(contentx))
        FeatureDate.run(contentx)

        del self.outstanding[name.toUri()]
        self.isDone = True




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







