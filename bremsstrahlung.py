import numpy as np
import main
import scipy.constants as con
import matplotlib.pyplot as plt

## E1, E2: energy (eV) of spectral peaks
E1 = 1188
E2 = 1218.5
## A, B are constants in the bremsstrahlung equation
A = 5*10**-42
B = 0.0149
## T: temp of plasma
T = 5*con.mega
## n: number of charge carriers per unit volume in plasma
n = 10**14
##standard deviation of spectral peaks in eV. FWHM = 2*sigma*(2ln2)^0.5
peak_sigma = 1.5

def lineout():
    for i in range(len(data)):
        y = np.sum(data[i], axis=0)
        y = np.delete(y, np.s_[:6])
        x = np.arange(1100.0, 1600.0, (1600.0-1100.0)/float(len(y)))
        if i in main.good:
            title = 'good'
        else:
            title = 'bad'
        main.plot(y, title, x)

## Inputs: temperature; density of charge carriers; physical constants A & B
## Outputs: 2048 evenly spaced wavelengths & energies; bremsstrahlung intensity
def brem(T, n, A=A, B=B):
    ## wave_lengths = range of wavelengths
    wave_lengths = np.linspace(0.77*con.nano, 1.13*con.nano, 2048)
    ## E = range of energies
    E = con.h*con.c/(con.e*wave_lengths)

    ## bremsstrahlung intensity
    y = A*(n**2)*np.exp(-B/(wave_lengths*T))/((T**0.5)*wave_lengths**2)

    return wave_lengths, E, y

## normal distribution
def norm(x, mu, sigma):
    return np.exp(-0.5*((x-mu)/sigma)**2)/(2*np.pi*sigma)

## creates L series normal peaks
def lseries(x, sigma, E1, E2):

    La1 = norm(x, E1, sigma)
    La2 = norm(x, E2, sigma)

    return La1, La2

## code to call functions to create bremsstrahlung with spectral peaks
def total(T=T, n=n):
    wave_lengths, E, brem1 = brem(T, n, A, B)
    La1, La2 = lseries(E, peak_sigma, E1, E2)

    return E, brem1 + 2*La1 + 2*La2
