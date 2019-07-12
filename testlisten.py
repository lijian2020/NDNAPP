import os
import time
import datetime
import pyinotify
import logging


def printline():
    pos = 0
    while True:
        try:
            with open(r'./abc.txt') as f:
                if pos != 0:
                    f.seek(pos, 0)
                while True:
                    line = f.readline()
                    if line.strip():
                        print(line.strip())
                        linestr = line.strip()
                        parseline(linestr)

                    pos = pos + len(line)
                    if not line.strip():
                        break
        except:
            print('error in open log file')


def parseline(linestr):
    linelist = linestr.split()
    if (linelist[5]):
        print(linelist[5])
    else:
        print('there is no linelist[5]')

if __name__ == '__main__':
    printline()
