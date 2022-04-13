import numpy as np
import UI
import main
import bremsstrahlung as bre
import scipy.constants as con

T = 150
T = T*con.e/con.k
print(T)
lam_, E_, y_ = bre.brem(T, bre.n, bre.A, bre.B)
main.plot1D(y_, E_)

## E: 2048 energies spanning full range (1100 - 1600 eV)
## rel_int: relative intensity of X-rays as a function of energy
E, rel_int = bre.total(T, n=5*10**14)

main.plot1D(rel_int, E, style='r--')

probability = rel_int / max(rel_int)

main.plot1D(probability, E, style='r--')

# creates array of positions of photon events
def make_photons(prob):
    prob = prob / 50
    photons = np.zeros((main.dim, main.dim))
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

photons, count, multicount, pixels, phoflat = make_photons(probability)
print(count, 'photons')
print('spanning', pixels, 'pixels')
print(multicount, 'of which where in multi photon events')
print(np.max(photons), 'is the most photons on 1 pixel')
main.plot2D(photons, 'photon events')
main.plot2D(phoflat, 'flattened photon events')
main.hist(photons, title='Histogram: number of photons per pixel')
