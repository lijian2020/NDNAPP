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
from oscommand import OSCommand


# This class is used to process control information data and includes some methods
# which are used for parsing the original data.
# So this class is normally no need to be instantiated
class CtrlInfo_Operation(object):

    def __init__(self):
        pass

    def run(self, ctrlinfo_raw_data):
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
