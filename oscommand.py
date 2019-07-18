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

'''This module is used to execute linux system commands, the purpose is just for convenience'''

import subprocess


class OSCommand(object):

    @staticmethod
    def getnodeid():
        command_output = subprocess.check_output(["ifconfig | grep eth0"], shell=True)
        nodeid = str(command_output.split(b'-')[0],'utf-8')
        return nodeid


    @staticmethod
    def getface():
        nodeid=OSCommand.getnodeid()
        command_output = subprocess.check_output(["export HOME=/tmp/minindn/{0} && nfdc face ". \
                                format(nodeid)], shell=True)
        return command_output

    @staticmethod
    def addrouttoRIB(prefix, face_id):
        nodeid = OSCommand.getnodeid()
        command_output = subprocess.check_output(["export HOME=/tmp/minindn/{0} && nfdc route add {1} {2} ". \
                                                 format(nodeid, prefix, face_id)], shell=True)
        return command_output



    @staticmethod
    def getFIB():
        nodeid=OSCommand.getnodeid()
        command_output = subprocess.check_output(["export HOME=/tmp/minindn/{0} && nfdc fib | grep / ". \
                                format(nodeid)], shell=True)
        return command_output

    @staticmethod
    def facemod(FaceMod_Operate_list):  # the list pattern:  [faceid   operation_code]
        nodeid = OSCommand.getnodeid()
        if (FaceMod_Operate_list[1] == '0x0001'):  # destroy a face
            command_output = subprocess.check_output(["export HOME=/tmp/minindn/{0} && nfdc face destroy {1}". \
                                                     format(nodeid, FaceMod_Operate_list[0])], shell=True)
            return command_output

        elif (FaceMod_Operate_list[1] == '0x0000'):  # add a create
            command_output = subprocess.check_output(["export HOME=/tmp/minindn/{0} && nfdc face create {1}". \
                                                     format(nodeid, FaceMod_Operate_list[0])], shell=True)
            return command_output

        else:  # Wrong code
            return "Wrong FaceMod Option Id"
