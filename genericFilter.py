import numpy as np
from scipy import ndimage
import UI
import main
import math
#import Energy_assignB
#import getFits
import matplotlib.pyplot as plt
import pickle

#plt.hist(UI.function(6).flatten(), bins=300, range=(0, 300))
#plt.show()

with open('pickleSynData.pk', 'rb') as fi:
    synData = pickle.load(fi)


data = UI.function(8)
plt.hist(data.flatten(), bins=300, range=(0, 300), log=True)
plt.show()

# calculate mu: mean of the pedestal & sig: standard deviation of pedestal
mu, sig = main.ped_properties(data)
#mu = main.ped_peak(data)
print('mu is', mu)
print('sig is', sig)

print(data[164, 665:667])
print(data[1394:1397, 1757])
print(data[1394:1398, 1758])
print(data[1395:1398, 1759], '\n')
#main.hist(data)
threshold = 120
threshMinor = mu + 3*sig
## sillyThresh to check for erroneously large sums
sillyThresh = 900
## count number of points removed for being erroneously large
RmvCnt = 0
coMajor = 0
coLocSum = 0
coMultiPho = 0
coAdj = [0,0,0,0,0,0,0,0,0,0]
var1 = [0,0,0,0,0,0,0,0,0,0,0]
var2 = []
var3 = []
sinPhoVals = []
spreadPhoVals = []
sing = []
ding = []
count = 0
index = [0,-1]
lowpho = []
error = np.zeros((2048, 2048))

input = np.array([[1,1,1],
                  [1,1,1],
                  [1,1,1]])

input2 = np.array([[1,1,1,1,1],
                   [1,1,1,1,1],
                   [1,1,1,1,1],
                   [1,1,1,1,1],
                   [1,1,1,1,1]])

def sum(a, thrMaj, thrMin, silThr):
    ## checks single pixel peak
    global coMajor
    ## counts # of single pixel peaks with small local sums
    global coLocSum
    ## counts # of single pixel peaks with no local pixels > 80
    global coAdj
    global coMultiPho
    global sinPhoVals
    global spreadPhoVals
    global sing
    global ding
    global mu
    global var1
    global var2
    global var3
    global count
    global lowpho
    global index
    index[1] = index[1] + 1
    if index[1] == main.dim:
        index[0] = index[0] + 1
        index[1] = 0
    if a[4] > thrMaj:
        tot = a.sum() - a[4]
        if tot > silThr:
            global RmvCnt
            RmvCnt += 1
            #print(a[4])
            return 0
        coMajor += 1
        # check if edge or corner pixel. 3->edge 5->corner
        zeros = list(a).count(0)
        if tot < mu*8 + 3*sig*8**0.5:
            coLocSum += 1
        z=0
        ding.append(a[4]-mu)
        for i in range(len(a)):
            if a[i] > thrMaj and i != 4:
                coMultiPho += 1
                lowpho.append((a.sum() - mu*(9-zeros))/120)
                if lowpho[-1] > 0.8 and a[4] == max(a):
                    var2.append(max(a))
                    if var2[-1] < 102:
                        print(3)
                        print(a, '\n')
                break
            if a[i] > thrMin and i != 4:
                z += 1
            if i == len(a) - 1:
                coAdj[z] += 1
                sing.append(tot + a[4] -mu*(9-zeros))
                lowpho.append((a.sum() - mu*(9-zeros))/120)
                if lowpho[-1] > 0.8 and a[4] == max(a):
                    var2.append(max(a))
                    if var2[-1] < 102:
                        print(2)
                        print(a, '\n')
                if z == 0:
                    sinPhoVals.append(tot + a[4] - mu*(9-zeros))
                else:
                    spreadPhoVals.append(tot + a[4] - mu*(9-zeros))

        return tot
    elif a[4] > 70:
        x1 = [i for i in a if i > thrMaj]
        if len(x1) > 0:
            return 0
        count += 1
        zeros = list(a).count(0)

        lowpho.append((a.sum() - mu*(9-zeros))/120)
        if lowpho[-1] > 0.8 and a[4] == max(a):
            var2.append(max(a))
            if var2[-1] > 102:
                print(1)
                print(index)
                print(a, '\n')
                var3.append(index.copy())
        return 0
    else:
        return 0

## look 2 pixels away (tot will be 3* larger than 1 pixel away)
def sum2(a, thrMaj, thrMin, silThr):
    ## checks single pixel peak
    global coMajor
    ## counts # of single pixel peaks with small local sums
    global coLocSum
    ## counts # of single pixel peaks with no local pixels > 80
    global coAdj
    global coMultiPho
    global sinPhoVals
    global spreadPhoVals
    global sing
    global ding
    global mu
    global var1
    global var2
    #zeros = list(a).count(0)
    #var2.append(a.sum() - mu*(25-zeros))
    if a[12] > thrMaj:
        tot = a.sum() - a[12]
        if tot > silThr*3:
            global RmvCnt
            RmvCnt += 1
            #print(a[4])
            return 0
        coMajor += 1
        # check if edge or corner pixel. 3->edge 5->corner
        zeros = list(a).count(0)
        if tot < mu*10.4*3:
            coLocSum += 1
        z=0
        indexes = [6,7,8,11,12,13,16,17,18]
        for i in indexes:
            if a[i] > thrMaj and i != 12:
                coMultiPho += 1
                break
            if a[i] > thrMin and i != 12:
                z += 1
            if i == indexes[-1]:
                coAdj[z] += 1
                sing.append(tot + a[12] -mu*(25-zeros))
                ding.append(a[12]-mu)
                if z == 0:
                    sinPhoVals.append(tot + a[12] - mu*(25-zeros))
                else:
                    spreadPhoVals.append(tot + a[12] - mu*(25-zeros))
                if z > 1 and (tot + a[12] -mu*(25-zeros))/120 < 1.5:
                    print(tot + a[12] -mu*(25-zeros))
                    print((tot + a[12] -mu*(25-zeros))/120)
                    print(a[0:5])
                    print(a[5:10])
                    print(a[10:15])
                    print(a[15:20])
                    print(a[20:25], '\n')
        return tot
    else:
        return 0

def SPC(a, thrMaj, thrMin, silThr):
    ## checks single pixel peak
    global coMajor
    ## counts # of single pixel peaks with small local sums
    global coLocSum
    ## counts # of single pixel peaks with no local pixels > 80
    global coAdj
    global coMultiPho
    global sinPhoVals
    global spreadPhoVals
    global sing
    global ding
    global mu
    global var1
    global var2
    global count
    global error
    global index
    index[1] = index[1] + 1
    if index[1] == main.dim:
        index[0] = index[0] + 1
        index[1] = 0
    #zeros = list(a).count(0)
    #var2.append(a.sum() - mu*(25-zeros))
    if a[12] > thrMaj:
        centre_indexes = [6,7,8,11,12,13,16,17,18]
        outer_indexes = [0,1,2,3,4,5,9,10,14,15,19,20,21,22,23,24]
        cen = np.array([a[i] for i in centre_indexes])
        out = np.array([a[i] for i in outer_indexes])

        centot = cen.sum() - a[12]
        if centot > silThr:
            global RmvCnt
            RmvCnt += 1
            #print(a[4])
            return 0
        coMajor += 1
        # check if edge or corner pixel. 10->edge 16->corner
        cenzeros = list(cen).count(0)

        z=0
        m=0
        for i in range(len(cen)):
            if cen[i] > thrMaj and i != 4:
                coMultiPho += 1
                m += 1
            elif cen[i] > thrMin and i != 4:
                z += 1
            if i == len(cen) - 1:
                coAdj[z] += 1
                sing.append(centot + a[12] -mu*(25-cenzeros))
                ding.append(a[12]-mu)
                if m > 0:
                    for i in outer_indexes:
                        if a[i] > thrMaj:
                            m += 1
                    tot = a.sum()
                    samp = (tot - mu*(25-list(a).count(0)))/(130*m)
                    simp = (tot - mu*(25-list(a).count(0)))/(190*m)
                    error[index[0]][index[1]] += abs(round(samp - simp))
                    return samp
                if z == 0:
                    return round((cen.sum() - mu*(9-cenzeros))/150)
                else:
                    #sinPhoVals.append(centot + a[12] - mu*(25-cenzeros))
                    samp = (cen.sum() - mu*(9-cenzeros))/120
                    simp = (cen.sum() - mu*(9-cenzeros))/190
                    error[index[0]][index[1]] += abs(round(samp - simp))
                    return round((cen.sum() - mu*(9-cenzeros))/150)

        return 1
    elif a[12] > thrMin:
        x1 = [i for i in a if i > thrMaj]
        if len(x1) > 0:
            return 0

        centre_indexes = [6,7,8,11,12,13,16,17,18]
        outer_indexes = [0,1,2,3,4,5,9,10,14,15,19,20,21,22,23,24]
        cen = np.array([a[i] for i in centre_indexes])
        out = np.array([a[i] for i in outer_indexes])
        centot = cen.sum() - a[12]
        zeros = list(cen).count(0)

        lowpho = (cen.sum() - mu*(9-zeros))/120
        if lowpho > 0.9 and cen[4] == max(cen):
            count += 1
            error[index[0]][index[1]] += abs(round(lowpho - lowpho*120/190))
            return lowpho
        else:
            return 0
    else:
        return 0

#cnt, pos = manualCount(data, threshold)
sums = ndimage.generic_filter(data, SPC, footprint=input2, mode='constant', origin=(0, 0), extra_arguments=(threshold, threshMinor, sillyThresh))
#with open('picklePhoPos(6).pk', 'wb') as fi:
#    pickle.dump(sums, fi)
#with open('picklePhoPosError(6).pk', 'wb') as fi:
#    pickle.dump(error, fi)
print(coMajor, 'counts')
print(count, 'points at edge of pedestal with no local major pixel')
print(RmvCnt, 'erroneously large points were removed')
print(coLocSum, 'counts with sum <', round(mu*8 + 3*sig*8**0.5), '(single photon with spread within pedestal gausian)')
print(coAdj[0], 'counts with adjacent pixels all <', threshMinor, '(no spread pixel out of pedestal)')
print(coMultiPho, 'counts with many adjacent photon events')
print(coAdj)
print(np.array(coAdj)/np.array(coAdj).sum())
print(sinPhoVals)
print('\n', lowpho)
plt.hist(lowpho, bins=100)
plt.title('possible non major events')
plt.show()
#plt.hist(var2, bins = int(max(var2) - min(var2)))
#plt.title('major pixel in photon events')
#plt.show()

def allelse():
    with open('pickleSynPos.pk', 'rb') as fi:
        photons = pickle.load(fi)
        pp = []
    print(var3)
    for i in range(len(var3)):
        j = var3[i][0]
        k = var3[i][1]
        print(i)
        print(j, k)
        if j == 2047 or j == 0 or k == 2047 or k == 0:
            print('continue')
            continue
        pp.append(photons[j][k])
        print(photons[j-1][k-1],photons[j-1][k],photons[j-1][k+1])
        print(photons[j][k-1],photons[j][k],photons[j][k+1])
        print(photons[j+1][k-1],photons[j+1][k],photons[j+1][k+1], '\n')
    plt.hist(pp, bins = 5)
    plt.show()

    print('\n', len(lowpho))
    x6 = []
    for i in range(len(lowpho)):
        if lowpho[i] < 0.5:
            x6.append(lowpho[i])
    print(len(x6))
    print(len([i for i in lowpho if i < 0.9]))
    print(len([i for i in lowpho if i < 0.8]))
    print(len([i for i in lowpho if i < 0.7]))

def plots():
    plt.hist(sinPhoVals, bins=100)
    plt.title('pedestal removed 9 pixel sum of single pixel hits')
    plt.show()
    plt.title('ding - major pixel of all hits')
    plt.hist(ding, bins=150, density = True, range=(64, 214))
    plt.show()
    plt.title('major pixel of all hits')
    plt.hist(data.flatten(), bins=150, density = True, range=(121, 271))
    plt.show()
    plt.title('sing - ped removed 9 pix sum of all hits')
    plt.hist(sing, bins=75, range=(0,300))
    plt.show()
    plt.hist(spreadPhoVals, bins=75, range=(0,300))
    plt.title('pedestal removed 9 pixel sum of multi pixel hits')
    plt.show()
    #main.hist(sums, title=threshold)
    #main.hist(np.array(sinPhoVals))

#plots()

def eventEnergies():
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
