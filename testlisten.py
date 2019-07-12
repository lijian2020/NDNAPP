import os
import time
import datetime
import pyinotify
import logging


# pos = 0
# while True:
#     try:
#         with open(r'./abc.txt') as fd:
#             if pos != 0:
#                 fd.seek(pos, 0)
#             while True:
#                 line = fd.readline()
#                 if line.strip():
#                     print(line.strip())
#                     linestr = line.strip()
#                     linelist = linestr.split()
#                     print(linelist[0])
#
#                 pos = pos + len(line)
#                 if not line.strip():
#                     break
#     except:
#         print('error in open log file')
#
#


class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        try:
            pos = 0
            while True:
                try:
                    with open(r'./abc.txt') as fd:
                        if pos != 0:
                            fd.seek(pos, 0)
                        while True:
                            line = fd.readline()
                            if line.strip():
                                print(line.strip())
                                linestr = line.strip()
                                linelist = linestr.split()
                                print(linelist[0])

                            pos = pos + len(line)
                            if not line.strip():
                                break
                except:
                    print('error in open log file')


        except:
            print('error')


def main():
    # watch manager
    wm = pyinotify.WatchManager()
    wm.add_watch('./abc.txt', pyinotify.ALL_EVENTS, rec=True)

    # event handler
    eh = MyEventHandler()

    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()


if __name__ == '__main__':
    main()
