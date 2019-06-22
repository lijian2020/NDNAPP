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



class PrefixRouteTable(object):
    '''used to process and record Prefix by controller.  this table should be instant when controller
     starts.'''


    def __init__(self):
        self.prefixtable = np.array(['Oprefix', 'Iprefix', 'Ori', 1, 9999999999])
        self.starttime = time.time()
        self.endtime = time.time()
        self.tolc=Thread(target=self.timeoutloopcheck)
        self.tolc.start()


    "this is use another thread to monitoring_function a loop to check lifetime"
    def timeoutloopcheck(self):
        while True:
            self.updatelifetime()
            time.sleep(4)
            #print(self.prefixtable)   #just for test, should delete.


    """this method update the lifetime value,and delete items if it is out of time"""
    def updatelifetime(self):
        temp_prefixtable = self.prefixtable.copy()
        self.endtime = time.time()
        #time.sleep(10)
        timegap = self.endtime - self.starttime
        self.starttime =self.endtime

        temp_prefixtable[..., 4] = temp_prefixtable[..., 4].astype(np.float) - timegap
        tofloatlist = list(map(lambda x: float(x), temp_prefixtable[..., 4].tolist()))

        for i,j in enumerate(tofloatlist):
            if(j <= 0):
                temp_prefixtable = self.delitem(temp_prefixtable,i)

        self.prefixtable = temp_prefixtable.copy()




    """update the table using the original interest. It is can be used directly."""
    def updateprefixroutetable(self,originalinterest):
        parsedlist = self.parseinterest(originalinterest)  #['Oprefix' 'Iprefix' 'Ori' 'update' 'LT']

        if(len(parsedlist[2])>0 and (parsedlist[3] in [0,1]) and parsedlist[4]>0): # it can be updated
            num = self.searchitem(parsedlist[1])   #search if it is existed, return None if not
            if (num):  # it means existed, delete it first
                self.prefixtable = self.delitem(self.prefixtable, num)

            if(parsedlist[3]):   #Update = 1   #add item
                self.prefixtable = self.additem(self.prefixtable, parsedlist)
                return('Add the route successfully')
            return ('Delete the route successfully')
        else:
            return('Error in Adding prefix to controller, Parameters incorrect.' )



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
    def searchitem(self,prefix):
        if not(prefix.endswith('/')):    #add '/' in the end if necessary
            prefix = prefix + '/'

        if(prefix in self.prefixtable[..., 1]):
            num = list(self.prefixtable[..., 1]).index(prefix)
            return num
        else:
            return None


    '''parse the origional interest to a list with 5 elements '''
    def parseinterest(self,originalinterest):
        outerprefix = None
        innerprefix = None
        origion = None
        update = None
        lifetime = 3600
        try:
            full_prefix = originalinterest.getName().toUri()
            prefix_list = full_prefix.split('--')
            outerprefix = prefix_list[0]
            innerprefix = prefix_list[1]
            origion = prefix_list[2]
            update = prefix_list[3]
            lifetime = prefix_list[4]

            origion = origion.replace('/','') if origion.startswith('/') else origion
            update = update.replace('/','') if update.startswith('/') else update
            lifetime = lifetime.replace('/','') if lifetime.startswith('/') else origion

            try:
                update = int(update)
                lifetime = float(lifetime)
            except:
                pass
        except:
            pass

        return [outerprefix,innerprefix,origion,update,lifetime]



#below is just for test, should be delete later.
# testinterest = Interest('/ndn/controller/update/--/abc/def/--/b--/1/--/300')
# testinterest2 = Interest('/ndn/controller/update/--/lijian/gege/--/b--/1/--/500')
# testinterest3 = Interest('/ndn/controller/update/--/kaikai/xinxin/--/b--/1/--/10')
#
# test=PrefixTable()
# test.parseinterest(testinterest)
# print(test.outerprefix)
# print(test.innerprefix)
# print(test.origion)
# print(test.update)
# print(test.lifetime)

# test._updateprefixtable(testinterest)
# # print(test._prefixtable)
# time.sleep(1)
# test._updateprefixtable(testinterest2)
# # print(test._prefixtable)
# time.sleep(1)
# test._updateprefixtable(testinterest3)
#
#
# test.updatelifetime()
#
# print(test._prefixtable)