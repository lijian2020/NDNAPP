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
        # self.fib_status_record = ""
        # self.rib_status_record = ""

        # count the flapping time
        self.channels_flapping_time = 0
        self.faces_flapping_time = 0
        #self.fib_flapping_time = 0
        #self.rib_flapping_time = 0


    def run(self):
        while True:
            if self.status_update_checker():
                HelloReq().run(self.hello_version_number)
                # if (HelloReq().run(self.hello_version_number)):
                #     FeatureRes().run()
            time.sleep(1)

            # protect flapping case
            if (self.channels_flapping_time > 5 or \
                    self.faces_flapping_time > 5):
                time.sleep(300)  # become silent for 5 min

                self.channels_flapping_time = 0
                self.faces_flapping_time = 0
                #self.fib_flapping_time = 0
                #self.rib_flapping_time = 0





    def status_update_checker(self):
        '''check if anything changes'''
        updated = False
        channels_status_record = Channels_status_getter().run()
        faces_status_record = Faces_status_getter().run()
        #fib_status_record = Fib_status_getter().run()
        #rib_status_record = Rib_status_getter().run()

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

        # if (self.fib_status_record != fib_status_record):
        #     updated = True
        #     self.fib_flapping_time += 1
        # else:
        #     if (self.fib_flapping_time > 0):
        #         self.fib_flapping_time -= 1

        # if (self.rib_status_record != rib_status_record):
        #     updated = True
        #     self.rib_flapping_time += 1
        # else:
        #     if (self.rib_flapping_time > 0):
        #         self.rib_flapping_time -= 1

        if (updated):
            print('\n ************* Node Status Changes *************\n')
            self.hello_version_number += 1
            # update the record
            self.channels_status_record = channels_status_record
            self.faces_status_record = faces_status_record
            #self.fib_status_record = fib_status_record
            #self.rib_status_record = rib_status_record

        return updated

#
#
# if __name__ == '__main__':
#     Status_Monitor().status_update_checker()
