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


'''This class is used for creating two global tables and includes some methods
which are used for parsing original feature content.
'''

import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)  #suppress future warnings globally

class FeatureDate(object):
    '''used to process and record all nodes' faces.These two tables are global variables which can be
    access according to [class name.variable name]'''
    FIB_array = np.empty(shape=[0, 10])  # a list including all nodes' FIB info
    # [node-id, prefix, next-hop,cost,next-hop,cost,next-hop,cost,None,None,]
    Face_array = np.empty(shape=[0, 10])  # a list including all nodes' Face info
    # [node-id, face-id, remote, local, congestion, mtu, counters, flags, None, None]

    def __init__(self):
        pass


    #below setters and getters haven't been used til now
    def _set_FIB_array(self,temp_FIB_array):
        FeatureDate.FIB_array = temp_FIB_array
    def _set_Face_array(self,temp_Face_array):
        FeatureDate.Face_array = temp_Face_array
    def _get_FIB_array(self):
        return FeatureDate.FIB_array
    def _get_Face_array(self):
        return FeatureDate.Face_array


    #these methods are only used for parsing the original feature data, no need to instantiate the class
    @staticmethod
    def run(featuredata):

        result = featuredata.split('----')
        nodeid = result[0].replace("b'", "")
        originFace_Data = result[1]
        originFIB_Data = result[2]

        temp_Face_array = FeatureDate.parseOriginFace_Date(nodeid,originFace_Data) #get an array including new FIB items
        if(nodeid in FeatureDate.Face_array[:,0:1]):
            pass
        FeatureDate.Face_array = np.row_stack((FeatureDate.Face_array, temp_Face_array))

        temp_FIB_array = FeatureDate.parseOriginFIB_Data(nodeid, originFIB_Data) #get an array including new FIB items
        if (nodeid in FeatureDate.FIB_array[:, 0:1]):
            pass
        FeatureDate.FIB_array = np.row_stack((FeatureDate.FIB_array, temp_FIB_array))

        #return temp_Face_array, temp_FIB_array
        np.savetxt(r'/tmp/minindn/Face_array.txt', FeatureDate.Face_array, fmt='%s %s %s %s %s %s %s %s %s %s')
        np.savetxt(r'/tmp/minindn/FIB_array.txt', FeatureDate.FIB_array, fmt='%s %s %s %s %s %s %s %s %s %s')


    @staticmethod
    def parseOriginFIB_Data(nodeid, originFIB_Data):
        FIB = originFIB_Data.replace("\n", "----")
        FIB = FIB.replace("nexthops={", "====")
        FIB = FIB.replace("}", "")
        FIB = FIB.split("----")
        FIB1 = []
        FIB_array =  np.empty(shape=[0, 10]) #temporary use to store the FIB items
        for i in FIB:
            i = i.replace(' ', '')
            i = i.replace('(cost=', '====')
            i = i.replace(')', '')
            i = i.replace(' ', "")
            i = i.replace('========', '====')
            i = i.split("====")
            FIB1.append(i)

        for i in FIB1:
            temp_list = [None, None, None, None, None, None, None, None, None, None]
            b = 1
            for j in i:
                temp_list[0] = nodeid
                temp_list[b] = j
                b += 1
            FIB_array = np.row_stack((FIB_array, temp_list))
        return FIB_array


    @staticmethod
    def parseOriginFace_Date(nodeid,originFace_Data):

        face = originFace_Data.replace('\n', "----")
        face = face.replace('remote=', "====remote=")
        face = face.replace('local=', "====local=")
        face = face.replace('congestion=', "====congestion=")
        face = face.replace('mtu=', "====mtu=")
        face = face.replace('counters=', "====counters=")
        face = face.replace('flags=', "====flags=")
        face = face.split("----")

        face1 = []
        for i in face:
            i = i.split("====")

            face1.append(i)

        face_array = np.empty(shape=[0, 10])  # temporary use to store the face items
        for i in face1:
            temp_list = [None, None, None, None, None, None, None, None, None, None]
            b = 1
            for j in i:
                temp_list[0] = nodeid
                temp_list[b] = j
                b += 1
            face_array = np.row_stack((face_array, temp_list))
        return face_array


