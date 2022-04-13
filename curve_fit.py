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

## Inputs: xdata, ydata
## Output: ydata fitted to the input xdata
def fit(xdata, ydata):
    popt, pcov = curve_fit(con_sec, xdata, ydata)
#print(popt)
#print('hello', type(popt))
    popt2, pcov2 = curve_fit(con_sec, xdata, ydata, p0=popt)
#print(popt2)
    popt3, pcov3 = curve_fit(con_sec2, xdata, ydata, p0=np.append(popt2, -0.05))
#print(popt3, '\n', '\n')
    return con_sec2(xdata, *popt3)

def self_function():
    image_data = UI.function()

    sum_data = main.sum(image_data)

    ##Inputs: data; square size; number of squares per row; x_min; x_max; continuous True or False; square True or False
    line_data, lineX, lineY = two_line_fit.find_peaks(sum_data, 32, 1, 1380, 1550, True, True)
    xdata = np.array(lineX[0])
    #xdata = xdata - 890
    ydata = lineY[0]

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
