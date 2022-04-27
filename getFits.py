## Takes data input; outputs y vales of both fitted spectral lines & mean line separation

import numpy as np
import two_line_fit
import matplotlib.pyplot as plt
import least_squares_fit
import optimizeAlpha

## LOOP TO REMOVE ASKEW CURVE MODEL POINTS that deviate more than 'deviate'
def point_select(x, y):
    incr = 0
    deviate = 16
    for i in range(len(y) - 1):
        if abs(y[i+1+incr] - y[i+incr]) > deviate:
            y = np.delete(y, i+1+incr)
            x = np.delete(x, i+1+incr)
            incr -= 1
    return x, y

## Input: data
## Output: 2 arrays of 2048 y values of the 2 spectral lines
##              NO NUM = LOWER LINE (higher energy line)
##              2      = HIGHER LINE (lower energy line)
##       : mean separation of lines
def fit_data(data):
    fit, x, y = two_line_fit.find_peaks(data, 64, 1, 1230, 1390, cont=True, square=False)
    fit2, x2, y2 = two_line_fit.find_peaks(data, 64, 1, 1380, 1550, True, False)

    X, Y = point_select(x[0], y[0])
    X2, Y2 = point_select(x2[0], y2[0])

    ## Returns 2048 fitted y points
    yfitted, params = least_squares_fit.simpfit(X, Y, [1000, 0, 10**5, 0, 0, 0], paramreturn=True)
    yfitted2, params2 = least_squares_fit.simpfit(X2, Y2, [1000, 1, 10**5, 0.1, -100, 0], paramreturn=True)

    def angle(params):
        return 0.5*math.atan(params[3]/(params[0]-1))

    import math
    print('\n')
    print('Range of angles (degrees) between the axes of the CCD and the direction of energy propagation:')
    #print(angle(least_squares_fit.param_convert(*params)))
    print(angle(least_squares_fit.param_convert(*params))*180/math.pi)
    #print(angle(least_squares_fit.param_convert(*params2)))
    print(angle(least_squares_fit.param_convert(*params2))*180/math.pi, '\n')

    # Plots
    plt.plot(x[0], y[0], 'x', label='1218.5 eV anomalies')
    plt.plot(X, Y, 'x', label='local sum maxima')
    plt.plot(np.arange(2048), yfitted, label='curve fit')
    plt.plot(x2[0], y2[0], 'x', label='1188.0 eV anomalies')
    plt.plot(X2, Y2, 'x', label='local sum maxima')
    plt.plot(np.arange(2048), yfitted2, label='curve fit')
    plt.title('Emission line locations with curve fitting')
    plt.xlabel('x_ (pixels)')
    plt.ylabel('y_ (pixels)')
    plt.legend()
    plt.show()

    # Avereage line separation
    dif = yfitted2 - yfitted
    mean = sum(dif)/len(dif)
    print('Distance (pixels) between emission lines:')
    print(min(dif))
    print(max(dif), '\n')
    print('mean: ', mean )
    print('mid-range: ', (max(dif) + min(dif))/2 )
    print('partial mean: ', sum(dif[500:len(dif)])/len(dif[500:len(dif)]), '\n')

    # Obtain aptimized value for alpha
    alpha = optimizeAlpha.getAlpha(yfitted, yfitted2, mean, X, X2)

    return yfitted, yfitted2, mean, alpha
