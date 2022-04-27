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

#with open('pickleSynData.pk', 'rb') as fi:
#    synData = pickle.load(fi)


#data = UI.function(8)
#plt.hist(data.flatten(), bins=300, range=(0, 300), log=True)
#plt.show()

#main.hist(data)

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
mu = 0
count = 0
index = [0,-1]
lowpho = []
error = np.zeros((2048, 2048))

# finds photon event locations in a single set of input data
# returns array with photon number at each pixel
# returns uncertainty on photon number array
def locatePhotons(data):
    # calculate mu: mean of the pedestal & sig: standard deviation of pedestal
    global mu
    mu, sig = main.ped_properties(data)
    #mu = main.ped_peak(data)
    print('Mean and standard deviation of the pedestal of the slected data set:')
    print('mu =', mu)
    print('sigma =', sig, '\n')

    threshold = 120
    threshMinor = mu + 3*sig
    ## sillyThresh to check for erroneously large sums
    sillyThresh = 900
    ## count number of points removed for being erroneously large

    input2 = np.array([[1,1,1,1,1],
                       [1,1,1,1,1],
                       [1,1,1,1,1],
                       [1,1,1,1,1],
                       [1,1,1,1,1]])

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
                    #sing.append(centot + a[12] -mu*(25-cenzeros))
                    #ding.append(a[12]-mu)
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
                        error[index[0]][index[1]] += abs(round((samp - simp)/2))
                        return round((cen.sum() - mu*(9-cenzeros))/150)
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
                error[index[0]][index[1]] += abs(round((lowpho - lowpho*120/190)/2))
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
    print(coMajor, 'major counts (ADU > 120)')
    print(count, 'minor counts ( 120 > ADU >', threshMinor, ')')
    print(RmvCnt, 'erroneously large points were removed')
    #print(coLocSum, 'counts with sum <', round(mu*8 + 3*sig*8**0.5), '(single photon with spread within pedestal gausian)')
    print(coAdj[0], 'major counts with adjacent pixels all <', threshMinor, '(no spread pixel out of pedestal)')
    print(coMultiPho, 'major counts with adjacent pixels also over the major threshold')
    #print(coAdj)
    #print(np.array(coAdj)/np.array(coAdj).sum())
    #print(sinPhoVals)
    #print('\n', lowpho)

    global error
    return sums, error

    plt.hist(lowpho, bins=100)
    plt.title('possible non major events')
    plt.show()
    #plt.hist(var2, bins = int(max(var2) - min(var2)))
    #plt.title('major pixel in photon events')
    #plt.show()
