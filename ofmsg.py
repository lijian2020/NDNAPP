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

'''This module is used to create different kinds of message, the purpose is just for convenience'''

import sys
from pyndn import Interest
from pyndn import Data
from pyndn.security import KeyChain


class OFMSG(object):
    prefix_controller = '/ndn/ie/tcd/controller01/ofndn/'

    def __init__(self):
        self.keyChain = KeyChain()

    #Add the OF head to a String object. Format: '--/n1.0/[0-34]/0/0/'
    def add_of_head(self,msg_name,msg_type):
        if msg_type in range(0,40):
            msg_type = str(msg_type)
        else:
            return('Message Type is incorrect')
        namestr = msg_name + str("--/n1.0/{}/0/0/".format(msg_type))
        return str(namestr)



    #create a hello message using local node-id and feature number. reture an Interest
    def create_hello_req_interest(self,node_id,feature_SN=1):
        hello_name = self.add_of_head(self.prefix_controller,0) + \
                     str("--{0}--{1}".format(node_id,feature_SN)) + \
                     str("--/ndn/{0}-site/{0}/ofndn/feature".format(node_id))
        interest = Interest(hello_name)
        interest.setMustBeFresh(True)
        interest.setInterestLifetimeMilliseconds(4000)
        return interest

    # create a ctrlinfo message using local node-id and feature number. reture an Interest
    def create_ctrlinfo_req_interest(self, node_id, ctrlinfo_SN=100001):
        hello_name = self.add_of_head(self.prefix_controller, 36) + \
                     str("--{0}--{1}".format(node_id, ctrlinfo_SN))
        interest = Interest(hello_name)
        interest.setMustBeFresh(True)
        interest.setInterestLifetimeMilliseconds(999999999999)
        return interest



    # create a FeatureReq message using local node-id . reture an Interest
    def create_feature_req_interest(self,feature_req_interest_name):
        interest = Interest(feature_req_interest_name)
        interest.setMustBeFresh(True)
        interest.setInterestLifetimeMilliseconds(4000)
        return interest

    #create a packetin message using unknown prefix. reture an Interest
    def create_packetin_msg_interest(self, unknown_prefix, node_id):
        packetin_name = self.add_of_head(self.prefix_controller, 10) + "/--/" + node_id + "/--" + unknown_prefix
        # /ndn/ie/tcd/controller01/ofndn/--/n1.0/10/0/0/--/h2--/unknown_prefix
        interest = Interest(packetin_name)
        interest.setMustBeFresh(True)
        interest.setInterestLifetimeMilliseconds(4000)
        return interest

    # create a error message using unknown prefix. reture an Interest
    def create_error_msg_interest(self, error_prefix):
        packetin_name = self.add_of_head(self.prefix_controller, 1) + "/--" + error_prefix
        # /ndn/ie/tcd/controller01/ofndn/--/n1.0/10/0/0/--/unknown_prefix
        interest = Interest(packetin_name)
        interest.setMustBeFresh(True)
        interest.setInterestLifetimeMilliseconds(4000)
        return interest

    # create a flowremoved message using unknown prefix. reture an Interest
    def create_flowremoved_msg_interest(self,removed_prefix):
        frmsg_name = self.add_of_head(self.prefix_controller,11) + "/--" + removed_prefix
                        #/ndn/ie/tcd/controller01/ofndn/--/n1.0/11/0/0/--/removed_prefix
        interest = Interest(frmsg_name)
        interest.setMustBeFresh(True)
        interest.setInterestLifetimeMilliseconds(1000)
        return interest

    def create_packetout_msg_interest(self,PacketOut_suffix):
        packetout_name = self.add_of_head(self.prefix_h1,13) + "-----" + PacketOut_suffix
                        #/ndn/h1-site/he/ofndn/--/n1.0/13/0/0/-------/PacketOut_suffix
        interest = Interest(packetout_name)
        interest.setMustBeFresh(True)
        interest.setInterestLifetimeMilliseconds(1000)
        return interest

    def create_facemod_msg_interest(self,facemod_suffix):
        packetout_name = self.add_of_head(self.prefix_h1,16) + "-----" + facemod_suffix
                        #/ndn/h1-site/he/ofndn/--/n1.0/16/0/0/-------/PacketOut_suffix
        interest = Interest(packetout_name)
        interest.setMustBeFresh(True)
        interest.setInterestLifetimeMilliseconds(1000)
        return interest

    # create a Hello_res_data message using interest and data . reture a Data
    def create_hello_res_data(self, interest, hello_data):  #
        '''the hello_data here indicates the result of fetch feature from node'''
        return self.set_returndata(interest, hello_data, )

    # create a ErrorACK message using interest  . reture a Data
    def create_errorAck_data(self, interest, errormsg_data):  #
        return self.set_returndata(interest, errormsg_data, )

    # create a _ctrlinfo_res message using interest  . reture a Data
    def create_ctrlinfo_res_data(self, interest, CtrlInfo_data):  #
        return self.set_returndata(interest, CtrlInfo_data,)

    # create a flowmod data message using interest and data . reture a Data
    def create_flowmod_data(self, interest, flowmod_data):  #
        return self.set_returndata(interest,flowmod_data,)

    def error_msg(self):  #reserve mst_type = 1
        pass


    # create a FeatureRes message using interest and feature data . reture a Data
    def create_feature_res_data(self,interest,feature_data):
        return self.set_returndata(interest,feature_data)


    def set_returndata(self,interest, returndatacontent):
        interestName = interest.getName()
        data = Data(interestName)
        data.setContent(returndatacontent)   #suppose the returndatacontent is string
        hourMilliseconds = 0  # here I should set it 0 since it always need to fresh.
        data.getMetaInfo().setFreshnessPeriod(hourMilliseconds)
        self.keyChain.sign(data, self.keyChain.getDefaultCertificateName())  #need to cheek if it works here.
        return(data)





#test
# ofm = OFMSG()
#OFMSG.add_of_head('abc',5)
# print(ofm.create_feature_req_interest('ccc').getName())
# featurereq_interest =Interest('/ndn/b-site/b/ofndn/feature')
# print(featurereq_interest.getName())
# print(ofm.create_feature_res_data(featurereq_interest,'i love you').getName())
# print(ofm.create_hello_req_interest('ccc',2342).getName())
# print(ofm.create_packetin_msg_interest('/abc/def/hig/').getName())
# print(ofm.create_packetout_data(Interest('/abc/def'),'you love me').getContent())
