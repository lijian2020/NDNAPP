import os
import time
import datetime
import pyinotify
import logging


def printline():
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


printline()
