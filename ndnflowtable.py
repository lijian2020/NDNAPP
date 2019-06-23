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

import numpy as np
from featurereq import FeatureReq

#This class is used for create a global tables(NFT) and includes some methods
# which are used for parsing original hello interest name.
# So this class is normally no need to be instantiated
class NdnFlowTable(object):
    '''used to process and record Prefix by controller.  this table is a global table.'''
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

        if(FlowEntry not in NdnFlowTable.NFT) and (FlowModDataList[4]=='0x0000'):
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
        print(NdnFlowTable.NFT)   #todo(print NFT) for test
        print("===================================")
        np.savetxt(r'/tmp/minindn/{}/NFT.txt'.format(nodeid), NdnFlowTable.NFT, fmt='%s %s %s %s %s %s %s %s %s %s')



    """update the table using the original interest from PacketOut Msg. It is can be used directly."""
    @staticmethod
    def derectly_updatendnflowtable(FlowModDataList,nodeid):
        NdnFlowTable.NFT = NdnFlowTable.additem(NdnFlowTable.NFT, FlowModDataList)  # add

        print("==============NFT==================")
        #print("EP, Face, Prefix, Priority,Counter,Idle-Lifetime,Hard-lifetime,Action,Out-faces,Flag")
        print(NdnFlowTable.NFT)   #todo(print NFT) for test
        print("===================================")
        np.savetxt(r'/tmp/minindn/{}/NFT.txt'.format(nodeid), NdnFlowTable.NFT, fmt='%s %s %s %s %s %s %s %s %s %s')





    @staticmethod
    def additem(Fulltable,parsedlist):  #add table item with the list including 5 elements
        try:
            Fulltable = np.row_stack((Fulltable, parsedlist))  # insert one line at the end
        except:
            return ("add faild")
        return (Fulltable)

    @staticmethod
    def delitem(Fulltable,number):   #delete table item with the index number.
        try:
            Fulltable = np.delete(Fulltable,number,axis=0)
        except:
            return ("delete faild")
        return (Fulltable)   #TODO(lijian),printer for test, could be deleted


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
    def parse_FaceMod_Interest(original_FaceMod_Interest):
        FaceMod_Interest_Name = original_FaceMod_Interest.getName().toUri()

        FaceMod_suffix = FaceMod_Interest_Name.split('-----')[1]
        FaceMod_suffix_list = FaceMod_suffix.split('---')
        return FaceMod_suffix_list

