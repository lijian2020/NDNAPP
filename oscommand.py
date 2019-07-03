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
