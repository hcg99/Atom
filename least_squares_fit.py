import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import UI
import main
import two_line_fit


def residuals(f, xdat, ydat, popt):
    res = 0
    for i in range(len(xdat)):
        res += (f(xdat[i], *popt) - ydat[i])**2
    return res

def con_sec(x, a, b, c, d, e):
    return a + b*((c + d*(x**2) + e*x)**0.5)

def con_sec2(x, a, b, c, d, e, f):
    return a + b*((c + d*(x**2) + e*x)**0.5) + f*x

## Inputs: xdata (must be np.array), ydata
## Output: ydata fitted to full dim x
## Option to return parameters. coeffs will be returned in "param_convert" form
def fit(xdata, ydata, p0=[1000, 0, 10**5, 0, 0, 0], paramreturn=False):
    popt, pcov = curve_fit(con_sec2, xdata, ydata, p0=p0)
    print(popt)
#print('hello', type(popt))
    popt2, pcov2 = curve_fit(con_sec2, xdata, ydata, p0=popt)
    print(popt2)
    #popt3, pcov3 = curve_fit(con_sec2, xdata, ydata, p0=np.append(popt2, -0.05))
#print(popt3, '\n', '\n')
    if paramreturn == True:
        return con_sec2(np.arange(main.dim), *popt2), param_convert(*popt2)
    return con_sec2(np.arange(main.dim), *popt2)

def simpfit(xdata, ydata, p0=[1000, 0, 10**5, 0, 0, 0], paramreturn=False):
    popt, pcov = curve_fit(con_sec, xdata, ydata, p0=p0[:5])
    print(popt)
#print('hello', type(popt))
    popt2, pcov2 = curve_fit(con_sec, xdata, ydata, p0=popt)
    print(popt2)
    popt3, pcov3 = curve_fit(con_sec2, xdata, ydata, p0=np.append(popt2, -0.05))
    print(popt3, '\n', '\n')
    if paramreturn == True:
        return con_sec2(np.arange(main.dim), *popt3), param_convert(*popt2)
    return con_sec2(np.arange(main.dim), *popt3)

## Input paramaters used in con_sec2
## Output coeffs: y^2 + Ax^2 + By + Cx + Dxy + E = 0
def param_convert(a, b, c, d, e, f=0):
    ## x & y have units of CCD pixel width (13.5 um)
    ## so we convert into metres here
    pixel = 13.5 * 10**-6
    A = f**2 - (b**2)*d
    B = -2*a
    C = 2*a*f - (b**2)*e
    D = -2*f
    E = a**2 - (b**2)*c
    return A, B*pixel, C*pixel, D, E*pixel**2

def self_function():
    image_data = UI.function()

    sum_data = main.sum(image_data)

    ##Inputs: data; square size; number of squares per row; x_min; x_max; continuous True or False; square True or False
    line_data, lineX, lineY = two_line_fit.find_peaks(sum_data, 32, 1, 1380, 1550, True, True)
    xdata = np.array(np.delete(lineX, 0))
    #xdata = xdata - 890
    ydata = lineY.pop(0)

    curvey = fit(xdata, ydata)

    plt.plot(xdata, ydata)
    plt.plot(np.arange(main.dim), curvey)
    plt.show()

    #main.plot(lineY[0], 'title', lineX[0])
    #main.plot(line_data, 'sum data square = True')

    residue1 = residuals(con_sec, xdata, ydata, popt)
    residue2 = residuals(con_sec, xdata, ydata, popt2)
    residue3 = residuals(con_sec2, xdata, ydata, popt3)
    print('res 1', residue1)
    print('res 2', residue2)
    print('res 3; xy', residue3)

    plt.plot(xdata, ydata, 'x', label='raw data')
    plt.plot(xdata, con_sec(xdata, *popt), label='fit1')
    plt.plot(xdata, con_sec(xdata, *popt2), label='fit2')
    plt.plot(xdata, con_sec2(xdata, *popt3), label='fit3')
    plt.legend()
    plt.show()

#self_function()
