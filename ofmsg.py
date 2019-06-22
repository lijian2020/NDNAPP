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
from pyndn import Interest
from pyndn import Data
from pyndn.security import KeyChain


class OFMSG(object):
    '''.'''
    prefix_controller = '/ndn/ie/tcd/controller01/ofndn/'
    prefix_h1 = '/ndn/h1-site/h1/ofndn/'
    prefix_h2 = '/ndn/h2-site/h2/ofndn/'
    prefix_h3 = '/ndn/h3-site/h3/ofndn/'
    prefix_h4 = '/ndn/h4-site/h4/ofndn/'
    prefix_h5 = '/ndn/h5-site/h5/ofndn/'


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


    # create a FeatureReq message using local node-id . reture an Interest
    def create_feature_req_interest(self,feature_req_interest_name):
        interest = Interest(feature_req_interest_name)
        interest.setMustBeFresh(True)
        interest.setInterestLifetimeMilliseconds(4000)
        return interest

    #create a packetin message using unknown prefix. reture an Interest
    def create_packetin_msg_interest(self,unknown_prefix):
        packetin_name = self.add_of_head(self.prefix_controller,10) + "/--" + unknown_prefix
                        #/ndn/ie/tcd/controller01/ofndn/--/n1.0/10/0/0/--/unknown_prefix
        interest = Interest(packetin_name)
        interest.setMustBeFresh(True)
        interest.setInterestLifetimeMilliseconds(4000)
        return interest

    #create a packetin message using unknown prefix. reture an Interest
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



    # create a Controller_Listener message using interest and feature data . reture a Data
    def create_hello_res_data(self,interest,hello_data): #todo need to check the hello_response
        return self.set_returndata(interest,hello_data,)
    '''the hello_data here indicates the result of fetch feature from node'''


    # create a Controller_Listener message using interest and feature data . reture a Data
    def create_flowmod_data(self,interest,flowmod_data): #todo need to check the hello_response
        return self.set_returndata(interest,flowmod_data,)
    '''the hello_data here indicates the result of fetch feature from node'''





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
