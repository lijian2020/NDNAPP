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

'''This class is used for create a global tables(NFT) and includes some methods
which are used for parsing original hello interest name.'''

import numpy as np
from oscommand import OSCommand
from featurereq import FeatureReq

class NdnFlowTable(object):
    '''used to process and record Prefix by node.  this table is a global table.'''
    NFT = np.empty(shape=[0, 10])  # an array as flow table
    # [EthernetPrefix, Face, Prefix, Priority,Counter,Idle-Lifetime,Hard-lifetime,Action,Out-faces,Flag]

    def __init__(self):
        pass


    #below setter and getter haven't been used til now
    def _setter(self,temp_NFT):
        self.NFT = temp_NFT

    def _getter(self):
        return  self.NFT



    """update the table using the parsed Data from FlowMod msg. It is can be used directly."""
    @staticmethod
    def updatendnflowtable(FlowModDataList,nodeid):
        #FlowModDataList: [ep(0),face(1),prefix(2),cookie(3),command(4),idle_timeout(5),
        # hard_timeout(6), priority(7),buffer_id(8),out_face(9),flag(10), action(11)]
        FlowEntry = [FlowModDataList[0],FlowModDataList[1],FlowModDataList[2], \
                     FlowModDataList[7],0,FlowModDataList[5],FlowModDataList[6], \
                     FlowModDataList[11],FlowModDataList[9],FlowModDataList[10]]
        # [EthernetPrefix(0), Face(1), Prefix(2), Priority(3),Counter(4),
        # Idle-Lifetime(5),Hard-lifetime(6),Action(7),Out-faces(8),Flag(9)]
        if (FlowEntry[2] not in NdnFlowTable.NFT[:, 2:3]) and (FlowModDataList[4] == '0x0000'):
            NdnFlowTable.NFT = NdnFlowTable.additem(NdnFlowTable.NFT,FlowEntry)  #add
        elif(FlowEntry in NdnFlowTable.NFT):
            num = NdnFlowTable.searchitem(FlowEntry[2])
            NdnFlowTable.delitem(NdnFlowTable.NFT,num)
            if (FlowModDataList[4] == '0x0003'): #delete
                pass
            elif(FlowModDataList[4]=='0x0001'):  #modify
                NdnFlowTable.NFT = NdnFlowTable.additem(NdnFlowTable.NFT, FlowEntry)  # add


        elif (FlowModDataList[4] == '0x0002'): #modify strict
            pass  # del

        elif (FlowModDataList[4] == '0x0004'): #delete strict
            pass  # del
        else:
            print("Wrong Flow Entry Command Code")
        print("==============NFT==================")
        #print("EP, Face, Prefix, Priority,Counter,Idle-Lifetime,Hard-lifetime,Action,Out-faces,Flag")
        print(NdnFlowTable.NFT)  # print NFT for test
        print("===================================")

        np.savetxt(r'/tmp/minindn/{}/NFT.txt'.format(nodeid), NdnFlowTable.NFT, fmt='%s %s %s %s %s %s %s %s %s %s')

    """update the table using the original interest from PacketOut Msg. It is can be used directly."""
    @staticmethod
    def derectly_updatendnflowtable(FlowModDataList,nodeid):
        NdnFlowTable.NFT = NdnFlowTable.additem(NdnFlowTable.NFT, FlowModDataList)  # add

        print("==============NFT==================")
        #print("EP, Face, Prefix, Priority,Counter,Idle-Lifetime,Hard-lifetime,Action,Out-faces,Flag")
        print(NdnFlowTable.NFT)  # rint NFT for test
        print("===================================")
        np.savetxt(r'/tmp/minindn/{}/NFT.txt'.format(nodeid), NdnFlowTable.NFT, fmt='%s %s %s %s %s %s %s %s %s %s')





    @staticmethod
    def additem(Fulltable,parsedlist):  #add table item with the list including 5 elements
        # [EthernetPrefix(0), Face(1), Prefix(2), Priority(3),Counter(4),
        # Idle-Lifetime(5),Hard-lifetime(6),Action(7),Out-faces(8),Flag(9)]
        try:
            Fulltable = np.row_stack((Fulltable, parsedlist))  # insert one line at the end
            OSCommand.addrouttoRIB(parsedlist[2], parsedlist[8])
            print('################# Add New Route ################\n')
            print("New route '{0}' has been added to RIB \n".format(parsedlist[2]))
            print('################################################\n')

        except:
            return ("add faild")
        return (Fulltable)

    @staticmethod
    def delitem(Fulltable,number):   #delete table item with the index number.
        try:
            Fulltable = np.delete(Fulltable,number,axis=0)
        except:
            return ("delete faild")
        return (Fulltable)


    """search if the entry existed in the table. p"""
    @staticmethod
    def searchitem(prefix):
        # NFT:[EthernetPrefix, Face, Prefix, Priority,Counter,Idle-Lifetime,Hard-lifetime,Action,Out-faces,Flag]
        if (prefix in NdnFlowTable.NFT[:, 2:3]):
            num = np.argwhere(NdnFlowTable.NFT == prefix)[0][0]  # line number:
            return num
        else:
            return None

    '''parse the received FlowMod Data to a list '''
    @staticmethod
    def parse_FlowMod_Data(original_FlowMod_Data):
        FlowMod_Data = original_FlowMod_Data.toRawStr()
        FlowMod_Data_list = FlowMod_Data.split('---')
        #  [ep(0),face(1),prefix(2),cookie(3),command(4),idle_timeout(5),hard_timeout(6), priority(7),
        #  buffer_id(8),out_port(9),flag(10), action(11)]
        return FlowMod_Data_list

    @staticmethod
    def parse_PacketOut_Interest(original_PacketOut_Interest):
        PacketOut_Interest_Name = original_PacketOut_Interest.getName().toUri()

        PacketOut_suffix = PacketOut_Interest_Name.split('-----')[1]
        PacketOut_suffix_list=PacketOut_suffix.split('---')
        return PacketOut_suffix_list

    @staticmethod
    def parse_Packetin_Interest(original_Packetin_Interest):
        # /ndn/ie/tcd/controller01/ofndn/--/n1.0/10/0/0/--/unknown_prefix

        PacketIn_Interest_Name = original_Packetin_Interest.getName().toUri()
        PacketIn_prefix_list = PacketIn_Interest_Name.split('--')

        return PacketIn_prefix_list[2], PacketIn_prefix_list[3]  # return node_id and unknown_prefix





    @staticmethod
    def parse_FaceMod_Interest(original_FaceMod_Interest):
        FaceMod_Interest_Name = original_FaceMod_Interest.getName().toUri()

        FaceMod_suffix = FaceMod_Interest_Name.split('-----')[1]
        FaceMod_suffix_list = FaceMod_suffix.split('---')
        return FaceMod_suffix_list

