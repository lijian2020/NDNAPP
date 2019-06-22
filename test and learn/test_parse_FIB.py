import numpy as np
with open('featuredata.txt','r') as f:
    featuredata = f.read()
result = featuredata.split('----')
nodeid = result[0].replace("b'","")
face = result[1]
FIB = result[2]


FIB = FIB.replace("\\n","----")
FIB = FIB.replace("nexthops={","====")
FIB = FIB.replace("}","")
FIB = FIB.split("----")
FIB1 = []
for i in FIB:
    i = i.replace(' ','')
    i = i.replace('faceid=', '====')
    i = i.replace('(cost=', '====')
    i = i.replace(')', '')
    i = i.replace(' ',"")
    i = i.replace('========', '====')
    i = i.split("====")
    FIB1.append(i)


FIB_array = np.empty(shape=[0, 7])  # a list including all nodes' advertised prefix


for i in FIB1:
    temp_list = [None, None, None, None, None, None, None]
    b = 1
    for j in i:

        temp_list[0]= nodeid
        temp_list[b]= j
        b+=1
        print(temp_list)
    FIB_array = np.row_stack((FIB_array, temp_list))



print(FIB_array)


