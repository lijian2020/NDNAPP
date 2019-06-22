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
import time
import numpy as np
from pyndn import Interest
from threading import Thread
from ofmsg import OFMSG
from featurereq import FeatureReq


class NodePrefixTable(object):
    '''used to process and record Prefix by controller.  this table should be instant when controller
     starts.'''


    def __init__(self):
        self.node_prefix_table = np.empty(shape=[0, 4])  # a list including all nodes' advertised prefix
        # [h1, version number, type_number, node_prefix]
        self.ofmsg = OFMSG()


        # self.starttime = time.time()
        # self.endtime = time.time()
        # self.tolc=Thread(target=self.timeoutloopcheck)
        # self.tolc.start()
        #

    # "this is use another thread to monitoring_function a loop to check lifetime"
    # def timeoutloopcheck(self):
    #     while True:
    #         self.updatenodeprefixtable()
    #         time.sleep(4)
    #         print(self.node_prefix_table)   #just for test, should delete.
    #




    """update the table using the original interest. It is can be used directly."""
    def updatenodeprefixtable(self, originalinterest):
        helloreq_name_prefix = self.parse_interest(originalinterest)
        #[h1, version number, type_number, node_prefix]
        if helloreq_name_prefix[0] in self.node_prefix_table[:, 0:1]:
            nodeindex = self.searchitem(helloreq_name_prefix[0])
            if helloreq_name_prefix[1] > int(self.node_prefix_table[nodeindex][1]):

                self.node_prefix_table = self.delitem(self.node_prefix_table, nodeindex)
                self.node_prefix_table = self.additem(self.node_prefix_table, helloreq_name_prefix)
                try:
                    FeatureReq().run(helloreq_name_prefix[3])
                    print('feature request has been sent out ')
                except:
                    print("FeatureReq send out fail XXXXXXXXXXX")
            else:
                print("the same hello message received")
        else:
            FeatureReq().run(helloreq_name_prefix[3])
            print('feature request has been sent out ')
            self.node_prefix_table = self.additem(self.node_prefix_table, helloreq_name_prefix)

        print(self.node_prefix_table)






    def additem(self,prefixtable,parsedlist):  #add table item with the list including 5 elements
        try:
            prefixtable = np.row_stack((prefixtable, parsedlist))  # insert one line at the end

        except:
            return ("add faild")
        return (prefixtable)

    def delitem(self,prefixtable,number):   #delete table item with the index number.
        try:
            prefixtable = np.delete(prefixtable,number,axis=0)
        except:
            return ("delete faild")
        return (prefixtable)




    """search if the prefix existed in the table. parameter prefix must be string started with "/"."""
    def searchitem(self,node_id):
        if(node_id in self.node_prefix_table[:, 0:1]):
            num = np.argwhere(self.node_prefix_table == node_id)[0][0] # line number:
            return num
        else:
            return None



    '''parse the origional Hello interest to a list '''
    def parse_interest(self,original_hello_interest):
        full_prefix = original_hello_interest.getName().toUri()
        prefix_temp_list = full_prefix.split('--')

        prefix_list = [prefix_temp_list[2],int(prefix_temp_list[3]),prefix_temp_list[1],prefix_temp_list[4]]
        #  [h1, version number, type_number, node_prefix]
        return prefix_list



# testinterest1 = Interest('/ndn/controller/update/--/n1.0/0/0/0/--h1--123--/ndn/h1-site/lijian/gege')
# testinterest2 = Interest('/ndn/controller/update/--/n1.0/0/0/0/--h2--456--/ndn/h1-site/kaikai/xinxin')
# testinterest3 = Interest('/ndn/controller/update/--/n1.0/0/0/0/--h3--789--/ndn/h1-site/I love you')
# testinterest4 = Interest('/ndn/controller/update/--/n1.0/0/0/0/--h2--897--/ndn/h1-site/kaikai/xinxin')
#
#
# test = NodePrefixTable()
# test.updatenodeprefixtable(testinterest2)
# test.updatenodeprefixtable(testinterest1)
# test.updatenodeprefixtable(testinterest3)
# test.updatenodeprefixtable(testinterest4)
# test.updatenodeprefixtable(testinterest2)
# print(test.node_prefix_table)
#
#

