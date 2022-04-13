import numpy as np
from scipy import ndimage
import UI
import main
#import Energy_assign
#import getFits
import matplotlib.pyplot as plt
import pickle

data = UI.function(1)
print(data[164, 665:667])
print(data[1394:1397, 1757])
print(data[1394:1398, 1758])
print(data[1395:1398, 1759], '\n')
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
co5 = 0
sinPhoVals = []
mu = main.ped_peak(data)

input = np.array([[1,1,1],
                  [1,1,1],
                  [1,1,1]])

def sum(a, thr, silThr):
    ## checks single pixel peak
    global co1
    ## counts # of single pixel peaks with small local sums
    global co2
    ## counts # of single pixel peaks with no local pixels > 80
    global co3
    global co4
    global co5
    global sinPhoVals
    global mu
    if a[4] > thr:
        co1 += 1
        tot = a.sum() - a[4]
        if tot > silThr:
            global RmvCnt
            RmvCnt += 1
            #print(a[4])
            return 0
        if tot < 500:
            co2 += 1
            return 1
        else:
            return 0
        for i in range(len(a)):
            if a[i] > thr and i != 4:
                co4 += 1
            if a[i] > 80 and i != 4:
                break
            if i == len(a) - 1:
                co3 += 1
                sinPhoVals.append(tot + a[4] - mu*9)
        return tot
    else:
        return 0



#cnt, pos = manualCount(data, threshold)
sums = ndimage.generic_filter(data, sum, footprint=input, mode='constant', origin=(0, 0), extra_arguments=(threshold, sillyThresh))
print(co1, 'counts')
print(RmvCnt, 'erroneously large points were removed')
print(co2, 'counts with sum < 500 (single photon with spread within pedestal gausian)')
print(co3, 'counts with adjacent pixels all < 80 (no spread pixel out of pedestal)')
print(co4, 'counts with many adjacent photon events')
#main.plot2D(sums)
#main.hist(sums, title=threshold)
#main.hist(np.array(sinPhoVals))


with open('pickleEmat.pk', 'rb') as fi:
    Emat = pickle.load(fi)

phoE = Emat * sums
phoE = [i for i in phoE.flatten() if i != 0]
print(phoE)


def hist(data, bins=100, title=''):
    plt.hist(data, bins=bins, log = True)
    plt.title(title)
    plt.show()

#hist(phoE, title='bins=100')
hist(phoE, bins=200, title='bins=200')
#hist(phoE, bins=50, title='bins=50')
