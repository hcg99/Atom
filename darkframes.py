import numpy as np
from scipy import ndimage
import UI
import main

data = UI.function(6)
#main.hist(data)
threshold = 120
## sillyThresh to check for erroneously large sums
sillyThresh = 900
## count number of points removed for being erroneously large
RmvCnt = 0
co1 = 0
co2 = 0
co3 = 0
co4 = 0
sinPhoVals = []
mu = data.sum()/(main.dim**2)

input = np.array([[1,1,1],
                  [1,1,1],
                  [1,1,1]])

def sum(a, thr, silThr):
    global co1
    global co2
    global co3
    global co4
    global sinPhoVals
    global mu

def dark_sum(data, div):
    avg = []
    edg = np.linspace(0, 2048, div+1)
    edg = edg.astype('int32')
    print(edg)
    for i in range(div):
        avg.append(data[edg[i]:edg[i+1]].sum()/(2048*(edg[i+1] - edg[i])))
    return avg


#cnt, pos = manualCount(data, threshold)
#sums = ndimage.generic_filter(data, sum, size=1, mode='constant', origin=(0, 0), extra_arguments=(threshold, sillyThresh))
dsum = np.array(dark_sum(data, 16))
print(dsum)
print('mu is ', mu)
print(dsum.sum()/16)
#main.plot2D(sums)
#main.hist(sums, title=threshold)
#main.hist(np.array(sinPhoVals))
tot = 0
for i in range(2048):
    tot += data[i].sum()
print(tot/2048**2)
