#!/usr/bin/python
#
# Copyright (C) 2019 Regents of the Trinity College of Dublin, the University of Dublin.
# Copyright (c) 2019 Susmit Li Jian
#
# Author: Li Jian <lij12@tcd.ie>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# A copy of the GNU General Public License is in the file COPYING.
#

import numpy as np
from featurereq import FeatureReq

#This class is used for create a global tables(NPT) and includes some methods
# which are used for parsing original hello interest name.
# So this class is normally no need to be instantiated
class NodePrefixTable(object):
    '''used to process and record Prefix by controller.  this table is a global table.'''
    NPT = np.empty(shape=[0, 4])  # a list including all nodes' advertised prefix
    # [h1, version number, type_number, node_prefix]

    def __init__(self):
        pass


    #below setter and getter haven't been used til now
    def _setter(self,temp_NPT):
        self.NPT = temp_NPT

    def _getter(self):
        return  self.NPT



    """update the table using the original interest. It is can be used directly."""
    @staticmethod
    def updatenodeprefixtable(originalinterest):
        helloreq_name_prefix = NodePrefixTable.parse_interest(originalinterest)
        featurereq_interest_prefix = str(helloreq_name_prefix[3]) + '/--/n1.0/0/0/0/'
        #[h1, version number, type_number, node_prefix]
        if helloreq_name_prefix[0] in NodePrefixTable.NPT[:, 0:1]:
            nodeindex = NodePrefixTable.searchitem(helloreq_name_prefix[0])
            if helloreq_name_prefix[1] > int(NodePrefixTable.NPT[nodeindex][1]):

                NodePrefixTable.NPT = NodePrefixTable.delitem(NodePrefixTable.NPT, nodeindex)
                NodePrefixTable.NPT = NodePrefixTable.additem(NodePrefixTable.NPT, helloreq_name_prefix)
                try:
                    FeatureReq().run(featurereq_interest_prefix)
                    print('feature request has been sent out ')
                except:
                    print("FeatureReq send out fail XXXXXXXXXXX")
            else:
                print("the same hello message received")
        else:
            FeatureReq().run(featurereq_interest_prefix)
            print('feature request has been sent out ')
            NodePrefixTable.NPT = NodePrefixTable.additem(NodePrefixTable.NPT, helloreq_name_prefix)

        #NodePrefixTable._setter(NodePrefixTable.NPT)
        print(NodePrefixTable.NPT)

        np.savetxt(r'/tmp/minindn/NPT.txt', NodePrefixTable.NPT,fmt='%s %s %s %s')


    @staticmethod
    def additem(prefixtable,parsedlist):  #add table item with the list including 5 elements
        try:
            prefixtable = np.row_stack((prefixtable, parsedlist))  # insert one line at the end

        except:
            return ("add faild")
        return (prefixtable)

    @staticmethod
    def delitem(prefixtable,number):   #delete table item with the index number.
        try:
            prefixtable = np.delete(prefixtable,number,axis=0)
        except:
            return ("delete faild")
        return (prefixtable)   #TODO(lijian),printer for test, could be deleted


    """search if the prefix existed in the table. parameter prefix must be string started with "/"."""
    @staticmethod
    def searchitem(node_id):
        if(node_id in NodePrefixTable.NPT[:, 0:1]):
            num = np.argwhere(NodePrefixTable.NPT == node_id)[0][0] # line number:
            return num
        else:
            return None



    '''parse the origional Hello interest to a list '''
    @staticmethod
    def parse_interest(original_hello_interest):
        full_prefix = original_hello_interest.getName().toUri()
        prefix_temp_list = full_prefix.split('--')

        prefix_list = [prefix_temp_list[2],int(prefix_temp_list[3]),prefix_temp_list[1],prefix_temp_list[4]]
        #  [h1, version number, type_number, node_prefix]
        return prefix_list

