## Takes data input; outputs y vales of both fitted spectral lines & mean line separation

import numpy as np
import two_line_fit
import matplotlib.pyplot as plt
import least_squares_fit

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

    # Plots
    plt.plot(x2[0], y2[0], 'x', label='2- all')
    plt.plot(X2, Y2, 'x', label='2 - removed')
    plt.plot(np.arange(2048), yfitted2, label='2 - fit')
    plt.plot(x[0], y[0], 'x', label='1 - all')
    plt.plot(X, Y, 'x', label='1 - removed')
    plt.plot(np.arange(2048), yfitted, label='1 - fit')
    plt.legend()
    plt.show()

    # Avereage line separation
    dif = yfitted2 - yfitted
    mean = sum(dif)/len(dif)
    print(min(dif), '\n',max(dif), '\n')
    print('mean: ', mean )
    print('mid-range: ', (max(dif) + min(dif))/2 )
    print('partial mean: ', sum(dif[500:len(dif)])/len(dif[500:len(dif)]), '\n')

    return yfitted, yfitted2, mean
