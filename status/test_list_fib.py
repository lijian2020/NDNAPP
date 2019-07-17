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

"""
This sends a fib list request to the local NFD and prints the response.
This is equivalent to the NFD command line command "nfd-status -r".
See http://redmine.named-data.net/projects/nfd/wiki/Management .
"""

import time
from pyndn import Face
from pyndn import Name
from pyndn import Interest
from pyndn.util import Blob
from pyndn.encoding import ProtobufTlv
from pyndn.util.segment_fetcher import SegmentFetcher
# This moudle is produced by: protoc --python_out=. fib-entry.proto
import fib_entry_pb2


def dump(*list):
    result = ""
    for element in list:
        result += (element if type(element) is str else str(element)) + " "
    print(result)


def main():
    # The default Face connects to the local NFD.
    face = Face()

    interest = Interest(Name("/localhost/nfd/fib/list"))
    interest.setInterestLifetimeMilliseconds(4000)
    dump("Express interest", interest.getName().toUri())

    enabled = [True]

    def onComplete(content):
        enabled[0] = False
        printFibEntries(content)

    def onError(errorCode, message):
        enabled[0] = False
        dump(message)

    SegmentFetcher.fetch(face, interest, None, onComplete, onError)

    # Loop calling processEvents until a callback sets enabled[0] = False.
    while enabled[0]:
        face.processEvents()

        # We need to sleep for a few milliseconds so we don't use 100% of the CPU.
        time.sleep(0.01)


def printFibEntries(encodedMessage):
    """
    This is called when all the segments are received to decode the
    encodedMessage as repeated TLV FibEntry messages and display the values.

    :param Blob encodedMessage: The repeated TLV-encoded FibEntry.
    """
    fibEntryMessage = fib_entry_pb2.FibEntryMessage()
    ProtobufTlv.decode(fibEntryMessage, encodedMessage)

    dump("FIB:");
    for fibEntry in fibEntryMessage.fib_entry:
        line = ""
        line += ProtobufTlv.toName(fibEntry.name.component).toUri()

        # Show the routes.
        for nexthop in fibEntry.next_hop_records:
            line += (" NextHopRecord={faceId=" + str(nexthop.face_id) + " cost=" + str(nexthop.cost))
            line += ")}"

        dump(line)


main()
