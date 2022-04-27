import numpy as np
import UI
import main
import pickle
import matplotlib.pyplot as plt
import getFits
import Energy_assign
import singlePhotonCount

# Input photon positions & energy matrix
# Output a list of all the photons energies
def phoEfct2(phoPos, Emat):
    phoE = []
    for i in range(2048):
        for j in range(2048):
            if phoPos[i][j] == 0:
                continue
            for k in range(round(phoPos[i][j])):
                phoE.append(Emat[i][j])
    return phoE

## index: sepcifies which data set out of the 20 you want to return a spectrum for
index = 11

# import list of 20 data sets
dataList = UI.function()
# sum all non-dark data sets
data = main.sum(dataList, main.good)

## fit the 2 spectral lines
## ylo & yup are coords for the 1218.5 & 1188.0 eV lines respectively in units of pixels
## dy is distance between lines
## alpha is the anlge between the normal vectors of the CCD and crystal diffraction plane
ylo, yup, dy, alpha = getFits.fit_data(data)

## get the energy matrix describing every CCD pixel with a photon energy value
Emat = Energy_assign.getEnergyMatrix(alpha, ylo, yup, dy)

## phoPos = photon number at each pixel
## error = uncertainty on phton number at each pixel
phoPos, error = singlePhotonCount.locatePhotons(dataList[index])
# convert photon positions to list of photon energies using the energy matrix
phoE = phoEfct2(phoPos, Emat)

## complete the above steps with the uncertainty both added and subtracted
phoPosEplus = phoPos.copy() + error.copy()
phoEplus = phoEfct2(np.around(phoPosEplus), Emat)

phoPosEminus = phoPos.copy() - error.copy()
phoEminus = phoEfct2(np.around(phoPosEminus), Emat)

# big, before-peak bins
bins1 = list(range(1088, 1160, 4))
# small, over-peak bins
bins2 = list(np.arange(1160, 1250, 2.5))
# big, after-peak bins
bins3 = list(range(1250, 1610, 5))
bins = bins1 + bins2 + bins3

# plot the spectrum
plt.hist(phoE, bins=bins, range=(1088,1625), log=True, density = True)
plt.title('X-ray emission spectrum - Data set ' + str(index))
plt.xlabel('photon energy (eV)')
plt.ylabel('relative intensity (a.u.)')
plt.show()

# plot the spectrum with uncertainty
plt.hist(phoEplus, bins=200, range=(1088,1625), log=True, label='upper bound')
plt.hist(phoEminus, bins=200, range=(1088,1625), log=True, label='lower bound')
plt.title('X-ray emission spectrum - Data set ' + str(index))
plt.xlabel('photon energy (eV)')
plt.ylabel('relative intensity (a.u.)')
plt.legend()
plt.show()
