
import math
import numpy as np
from scipy.optimize import curve_fit
import main
import scipy.constants as con

E1 = 1188
E2 = 1218.5
d = (15.954*10**-10)/2
the1 = math.asin((con.h*con.c)/(2*d*con.e*E1))
the2 = math.asin((con.h*con.c)/(2*d*con.e*E2))
## the1 (upper line) > the2 (lower line)

## Inputs: ylo = fitted y_ coords of 1218.5eV line
##          dy = distance between emission lines
##          x_ = x_ coords corresponding to ylo
##         x2_ = same as x_ but for the y_ of the 1188 eV line
## Output: value for alpha optimized using both fitted emission lines
def getAlpha(ylo, yup, dy, x_, x2_):

    ## function to model the 1218.5 eV emission line for a given alpha
    def f(x, a):
        P = dy / (1/math.tan(a + the2) - 1/math.tan(a + the1))
        A = (math.sin(a)/math.sin(the2))**2 - 1
        B = P*math.sin(2*a)/(math.sin(the2)**2)
        C = (P*math.cos(a)/math.sin(the2))**2 - x**2 - P**2
        #print((-B + (B**2 - 4*A*C)**0.5)/(2*A) + min(ylo) + P/math.tan(a+the2))
        return (-B + (B**2 - 4*A*C)**0.5)/(2*A) + min(ylo) + P/math.tan(a+the2)

    ## function to model the 1188.0 eV emission line for a given alpha
    def f2(x, a):
        P = dy / (1/math.tan(a + the2) - 1/math.tan(a + the1))
        A = (math.sin(a)/math.sin(the1))**2 - 1
        B = P*math.sin(2*a)/(math.sin(the1)**2)
        C = (P*math.cos(a)/math.sin(the1))**2 - x**2 - P**2
        #print((-B + (B**2 - 4*A*C)**0.5)/(2*A) + min(ylo) + P/math.tan(a+the2))
        return (-B + (B**2 - 4*A*C)**0.5)/(2*A) + min(ylo) + P/math.tan(a+the2)

    ## the following 'get' functions return constants to shift the origin of the
    ## x_, y_ coordinates to obtain x, y coordinates that are used in f() and f2()
    ## to model emission lines
    def getX():
        return [*ylo].index(min(ylo))

    def getX2():
        return [*yup].index(min(yup))

    def getY():
        global the2
        return min(ylo) + P/math.tan(a+the2)

    xdata1 = x_ - getX()
    ydata1 = [ylo[round(i)] for i in x_]

    xdata2 = x2_ - getX2()
    ydata2 = [yup[round(i)] for i in x2_]

    popt, pcov = curve_fit(f, xdata1, ydata1, p0=1)
    print('alpha optimized with 1218.5 eV line = ', popt)
    popt2, pcov2 = curve_fit(f2, xdata2, ydata2, p0=1)
    print('alpha optimized with 1188.0 eV line = ', popt2)
    alpha = (popt + popt2)/2
    print('mean alpha = ', (popt + popt2)/2, '\n')


    return alpha[0]
