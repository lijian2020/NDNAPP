import os
import time
import datetime
import pyinotify
import logging



pos = 0


def printlog():
    global pos
    try:
        with open(r'./abc.txt') as fd:
            if pos != 0:
                fd.seek(pos, 0)
            while True:
                line = fd.readline()
                if line.strip():
                    print(line.strip())
                pos = pos + len(line)
                if not line.strip():
                    break
    except:
        print("error")


class MyEventHandler(pyinotify.ProcessEvent):

    # 当文件被修改时调用函数
    def process_IN_MODIFY(self, event):
        try:
            printlog()
        except:
            print("error")


def main():
    # 输出前面的log
    printlog()
    # watch manager
    wm = pyinotify.WatchManager()
    wm.add_watch('./abc.txt', pyinotify.ALL_EVENTS, rec=True)
    eh = MyEventHandler()
    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    print('================')
    notifier.loop()


if __name__ == '__main__':
    main()
