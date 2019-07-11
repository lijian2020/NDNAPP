import os
import time

pos = 0
while True:
    # fd = open(r'./abc.txt')
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
# fd.close()
