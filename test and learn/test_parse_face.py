import numpy as np
with open('featuredata.txt','r') as f:
    featuredata = f.read()
result = featuredata.split('----')
nodeid = result[0].replace("b'","")
face = result[1]
FIB = result[2]



face = face.replace('\\n',"----")
face = face.replace('remote=',"====remote=")
face = face.replace('local=',"====local=")
face = face.replace('congestion=',"====congestion=")
face = face.replace('mtu=',"====mtu=")
face = face.replace('counters=',"====counters=")
#face = face.replace('out=',"====out=")
face = face.replace('flags=',"====flags=")
face = face.split("----")

face1 = []
for i in face:
    i = i.split("====")
    face1.append(i)


face_array = np.empty(shape=[0, 10])  # a list including all nodes' advertised prefix


for i in face1:
    temp_list = [None, None, None, None, None, None, None,None, None, None]
    b = 1
    for j in i:

        temp_list[0]= nodeid
        temp_list[b]= j
        b+=1
    face_array = np.row_stack((face_array, temp_list))



print(face_array)


