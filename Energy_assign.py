## Takes fitted curves as inputs and outputs 2048^2 array of pixel energies

import numpy as np
import UI
import getFits
import main
import math
import scipy.constants as con
import pickle

data = main.sum( UI.function(), main.good )
with open('pickledata.pk', 'wb') as fi:
    pickle.dump(data, fi)
## ylo & yup are in units of pixels
ylo, yup, dy = getFits.fit_data(data)

## Returns 2048^2 array of each pixels energy value
def getEnergyMatrix(P, a, ylo, yup):
    E1 = 1188
    E2 = 1218.5
    d = (15.954*10**-10)/2

    def getX():
        return [*ylo].index(min(ylo))

    def getY():
        return min(ylo) + P/math.tan(a+Ene2Ang(E2))

    ## Input energy, return bragg angle
    def Ene2Ang(E):
        return math.asin((con.h*con.c)/(2*d*con.e*E))

    ## Input sin(bragg angle), return energy
    def sinAng2Ene(sinAng):
        return (con.h*con.c)/(2*d*con.e*sinAng)

    X = getX()
    Y = getY()
    print(X, Y)

    EnergyMatrix = np.zeros((main.dim, main.dim))
    for x_ in range(main.dim):
        for y_ in range(main.dim):
            x = x_ - X
            y = y_ - Y
            EnergyMatrix[x_][y_] = sinAng2Ene((y*math.sin(a) + P*math.cos(a))/(x**2 + y**2 + P**2)**0.5)
            if E1-0.5 < EnergyMatrix[x_][y_] < E1+0.5:
                EnergyMatrix[x_][y_] += 20
            elif E2-0.5 < EnergyMatrix[x_][y_] < E2+0.5:
                EnergyMatrix[x_][y_] += 20

    return EnergyMatrix

#Emat = getEnergyMatrix(8.9/(13.5*10**-4), 0.8685, ylo, yup)
with open('pickleEmat.pk', 'rb') as fi:
    Emat = pickle.load(fi)

main.plot2D(Emat)

for i in range( main.dim ):
    Emat[i][round(ylo[i])] += 50
    Emat[i][round(yup[i])] += 50

main.plot2D(Emat)

## Input list of positions (indexes)
## Output list energies at the given positions
def getEnergyList(pos):
    Emat = getEnergyMatrix(8.9/(13.5*10**-4), 0.8685, ylo, yup)
    energies = []
    for i in range(len(pos)):
        energies.append(Emat[pos[i][0]][pos[i][1]])
    return energies
