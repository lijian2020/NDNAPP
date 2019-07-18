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
'''This module handles the CtrlInfo message. '''

import numpy as np
from featurereq import FeatureReq
from oscommand import OSCommand


# This class is used to process control information data and includes some methods
# which are used for parsing the original data.
# So this class is normally no need to be instantiated
class CtrlInfo_Operation(object):

    def __init__(self):
        pass

    def run(self, ctrlinfo_raw_data):
        # The structure and and basic function just list here, other functions need to be added in future work.
        CtrlInfo_data_list = self.parse_CtrlInfo_Data(ctrlinfo_raw_data)

        if (CtrlInfo_data_list[0] == '0x0000'):  # FlowMod
            pass


        elif (CtrlInfo_data_list[0] == '0x0001'):  # FaceMod
            FaceMod_Operate_list = [CtrlInfo_data_list[2], CtrlInfo_data_list[1]]
            OSCommand.facemod(FaceMod_Operate_list)


        elif (CtrlInfo_data_list[0] == '0x0002'):  # TableMod
            pass

        elif (CtrlInfo_data_list[0] == '0x0003'):  # Role
            pass

        elif (CtrlInfo_data_list[0] == '0x0004'):  # Error
            pass

        elif (CtrlInfo_data_list[0] == '0x0005'):  # CS
            pass

        elif (CtrlInfo_data_list[0] == '0x0006'):  # PrefixMod
            pass

        elif (CtrlInfo_data_list[0] == '0x0007'):  # Fib RouteMod
            pass

        else:
            pass

    @staticmethod
    def parse_CtrlInfo_Data(original_FaceMod_Data):
        CtrlInfo_data = original_FaceMod_Data.toRawStr()
        CtrlInfo_data_list = CtrlInfo_data.split('--')
        return CtrlInfo_data_list
