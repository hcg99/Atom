import numpy as np
import UI
import main
import bremsstrahlung as bre
import scipy.constants as con
import matplotlib.pyplot as plt
import pickle

lis1 = []

T = 150
T = T*con.e/con.k
print('T =', T)
lam_, E_, y_ = bre.brem(T, bre.n, bre.A, bre.B)
main.plot1D(y_, E_)

## E: 2048 energies spanning full range (1100 - 1600 eV)
## rel_int: relative intensity of X-rays as a function of energy
E, rel_int = bre.total(T, n=5*10**14)

main.plot1D(rel_int, E, style='r.')

probability = rel_int / max(rel_int)

main.plot1D(probability, E, style='r--')

# creates array of positions of photon events
def make_photons(prob):
    prob = prob / 80
    photons = np.zeros((main.dim, main.dim), 'int32')
    photonsflat = np.zeros((main.dim, main.dim))

    count = 0
    multicount = 0
    pixhit = 0
    for j in range(main.dim):
        for i in range(main.dim):
            ## photon number on each pixel modeled by poisson dist.
            photons[i][j] = np.random.poisson(prob[j])
            ## counts number of photons and multi photon events
            if photons[i][j] > 0:
                photonsflat[i][j] = 1
                pixhit += 1
                count += photons[i][j]
                if photons[i][j] > 1:
                    multicount += 1

    return photons, count, multicount, pixhit, photonsflat

# input photon positions; outputs adu values
def adu_spread(photons):
    # bloom is an array to store adu values due to photons
    bloom = np.zeros((main.dim, main.dim), 'int32')
    # meanADU is mean total ADU a single photon provides
    # this value will fluctualte normally using the fano factor for variance
    meanADU = 160
    sigma = 30
    # probability to determine magnitude of ADU spread for an event
    sprMean = 0.64
    # number of adjacent pixels that charge is spread to from a single photon
    # event is model by poisson distribution
    meanPixelSpread = 0.4
    z = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(main.dim):
        for j in range(main.dim):
            if photons[i][j] == 0:
                continue
            for k in range(photons[i][j]):
                total = np.random.normal(meanADU, sigma)
                lis1.append(total)
                if i == 0 or i == 2047 or j == 0 or j == 2047:
                    bloom[i][j] += total
                    continue
                spread = np.random.poisson(meanPixelSpread)
                if spread > 3:
                    spread = 3
                z[spread] += 1
                sprFactor = sprMean
                match spread:
                    case 0:
                        bloom[i][j] = bloom[i][j] + total
                        continue
                    case 1:
                        bloom[i][j] += total*sprFactor
                        p = round(np.random.rand())*2 - 1
                        q = round(np.random.rand())
                        if q == 0:
                            bloom[i+p][j] += total*(1-sprFactor)
                        else:
                            bloom[i][j+p] += total*(1-sprFactor)
                        continue
                    case 2:
                        bloom[i][j] += total*sprFactor**2
                        p = round(np.random.rand())*2 - 1
                        q = round(np.random.rand())*2 - 1
                        bloom[i+p][j] += total*(1-sprFactor)
                        bloom[i][j+q] += total*(1-sprFactor)*sprFactor
                        continue
                    case 3:
                        bloom[i][j] += total*sprFactor**3
                        p = round(np.random.rand())*2 - 1
                        q = round(np.random.rand())*2 - 1
                        bloom[i+p][j] += total*(1-sprFactor)
                        bloom[i][j+q] += total*(1-sprFactor)*sprFactor
                        bloom[i+p][j+q] += total*(1-sprFactor)*sprFactor**2
                        continue


    print(z)
    return bloom

## creates dim^2 array of random gaussian noise
def pedestal(mu=63, sig=10.6):
    norm = np.random.normal(loc=mu, scale=sig, size=(main.dim, main.dim))
    return norm

photons, count, multicount, pixels, phoflat = make_photons(probability)

with open('pickleSynPos.pk', 'wb') as fi:
    pickle.dump(photons, fi)
    
bloom = adu_spread(photons)

with open('pickleSynData.pk', 'wb') as fi:
    pickle.dump(bloom + pedestal(), fi)



main.hist(UI.function(6))
main.hist(bloom + pedestal())

print(count, 'photons')
print('spanning', pixels, 'pixels')
print(multicount, 'of which where in multi photon events')
print(np.max(photons), 'is the most photons on 1 pixel')
main.plot2D(photons, 'photon events')
main.plot2D(phoflat, 'flattened photon events')
main.hist(photons, title='Histogram: number of photons per pixel')

main.hist(adu_spread(photons))
plt.hist(lis1, bins=100)
plt.show()
