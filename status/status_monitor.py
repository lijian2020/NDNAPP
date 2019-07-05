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
from channels_status_getter import Channels_status_getter
from faces_status_getter import Faces_status_getter
from fib_status_getter import Fib_status_getter
from rib_status_getter import Rib_status_getter


class Status_Monitor(object):
    '''monitor the status changes '''

    def __init__(self):
        self.channels_status_record = ""

    def checker(self):
        channels_status_record = Channels_status_getter().run()

        faces_status_record = Faces_status_getter().run()

        fib_status_record = Fib_status_getter().run()

        rib_status_record = Rib_status_getter().run()

        print(rib_status_record)








if __name__ == '__main__':
    Status_Monitor().checker()
