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

import time

from ofmsg import OFMSG
from pyndn import Face
from oscommand import OSCommand
from helloreq import HelloReq
from featureres import FeatureRes

from status.channels_status_getter import Channels_status_getter
from status.faces_status_getter import Faces_status_getter
from status.fib_status_getter import Fib_status_getter
from status.rib_status_getter import Rib_status_getter


class Status_Monitor(object):
    '''monitor the status changes '''

    def __init__(self):
        self.ofmsg = OFMSG()

        self.hello_version_number = 200001

        # record the old record, which is used to compare to the new gotten ones
        self.channels_status_record = ""
        self.faces_status_record = ""
        self.fib_status_record = ""
        self.rib_status_record = ""

        # count the flapping time
        self.channels_flapping_time = 0
        self.faces_flapping_time = 0
        self.fib_flapping_time = 0
        self.rib_flapping_time = 0


    def run(self):
        while True:
            if self.status_update_checker():
                HelloReq().run(self.hello_version_number)
                # if (HelloReq().run(self.hello_version_number)):
                #     FeatureRes().run()
            time.sleep(10)

            # protect flapping case
            if (self.channels_flapping_time > 20 or \
                    self.faces_flapping_time > 20 or \
                    self.fib_flapping_time > 20 or \
                    self.rib_flapping_time > 20):
                time.sleep(300)  # become scient for 5 min

                self.channels_flapping_time = 0
                self.faces_flapping_time = 0
                self.fib_flapping_time = 0
                self.rib_flapping_time = 0





    def status_update_checker(self):
        '''check if anything changes'''
        updated = False
        channels_status_record = Channels_status_getter().run()
        faces_status_record = Faces_status_getter().run()
        fib_status_record = Fib_status_getter().run()
        rib_status_record = Rib_status_getter().run()

        '''anything changes will return True'''
        if (self.channels_status_record != channels_status_record):
            updated = True
            self.channels_flapping_time += 1
        else:
            if (self.channels_flapping_time > 0):
                self.channels_flapping_time -= 1

        if (self.faces_status_record != faces_status_record):
            updated = True
            self.faces_flapping_time += 1
        else:
            if (self.faces_flapping_time > 0):
                self.faces_flapping_time -= 1

        if (self.fib_status_record != fib_status_record):
            updated = True
            self.fib_flapping_time += 1
        else:
            if (self.fib_flapping_time > 0):
                self.fib_flapping_time -= 1

        if (self.rib_status_record != rib_status_record):
            updated = True
            self.rib_flapping_time += 1
        else:
            if (self.rib_flapping_time > 0):
                self.rib_flapping_time -= 1

        if (updated):
            print('********************* Node Status Changes **********************')
            self.hello_version_number += 1
            # update the record
            self.channels_status_record = channels_status_record
            self.faces_status_record = faces_status_record
            self.fib_status_record = fib_status_record
            self.rib_status_record = rib_status_record

        return updated

#
#
# if __name__ == '__main__':
#     Status_Monitor().status_update_checker()
