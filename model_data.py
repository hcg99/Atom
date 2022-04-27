import numpy as np
import UI
import matplotlib.pyplot as plt
import main

dim = 2048
data = UI.function()

def blank_array(dim):
    arr = [0]*dim
    arr = [arr]*dim
    return arr

## creates dim^2 array of random gaussian noise
## plot and histograms
def pedestal(data):
    norm = np.random.normal(loc=59, scale=8, size=(dim, dim))
    norm[0][0] = 350
    print(type(norm))
    main.plot2D(norm)
    main.hist(data[10])
    main.hist(norm)

pedestal(data)

## investigate the pedestal of all 20 images; min adu val, position of pedestal maximum
def ped_peak(data):
    good = []
    bad = []
    x = []
    y = []
    avgGd = np.array([0.0, 0.0])
    avgBd = np.array([0.0, 0.0])
    l = len(data)
    for i in range(l):
        [binVal, binEdg] = plt.hist(data[i].flatten(), bins=100, log=True)[:2]
        binVal = list(binVal)
        index = binVal.index((max(binVal)))
        peakPos = (binEdg[index] + binEdg[index + 1])/2
        if i in main.good:
            good.append([i, peakPos, binEdg[0]])
        else:
            bad.append([i, peakPos, binEdg[0]])
        x.append(peakPos - binEdg[1])
        y.append(peakPos)
        print(x)
        #plt.show()
    for i in main.good:
        avgGd += [y[i], x[i]]
    for i in main.bad:
        avgBd += [y[i], x[i]]
    avgGd = avgGd/len(main.good)
    avgBd = avgBd/len(main.bad)
    print(avgGd, avgBd)
    return good, bad


print(ped_peak(data))

#[x,y] = plt.hist(data[1].flatten(), bins=100, log = True)[:2]
#plt.yscale('log')
#print(x, '\n', 'first one done. length:', len(x))
#print(y, '\n', 'second one done. length:', len(y))
#X = list(x)
#index = X.index(max(x))
#bin = (y[index] + y[index + 1])/2
#print(bin)
#print(z, '\n', 'thrid one done')
#print(max(x))
#plt.show()
