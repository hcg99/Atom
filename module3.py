import numpy as np
import two_line_fit
import UI
import main
import matplotlib.pyplot as plt
import least_squares_fit
import math

data = main.sum( UI.function(), main.good )

fit, x, y = two_line_fit.find_peaks(data, 64, 1, 1230, 1390, cont=True, square=False)
fit2, x2, y2 = two_line_fit.find_peaks(data, 64, 1, 1380, 1550, True, False)
fit3, x3, y3 = two_line_fit.find_peaks(data, 64, 1, 1380, 1550, True, False)

print(type(fit))
#main.plot2D(-200*fit + -50*fit1 + data)
boundary = [1261, 1304, 1350]


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

def angle(params):
    return 0.5*math.atan(params[3]/(params[0]-1))


plt.plot(x2[0], y2[0], 'x', label='square')
plt.plot(x3[0], y3[0], 'x', label='line')

X, Y = point_select(x[0], y[0])
X2, Y2 = point_select(x2[0], y2[0])
X3, Y3 = point_select(x3[0], y3[0])

plt.plot(X2, Y2, 'x', label='sqare select')
plt.plot(X3, Y3, 'x', label='line select')
plt.legend()
plt.title('Upper Maxima')
plt.show()

plt.plot(x[0], y[0], 'x', label='line')
plt.plot(X, Y, 'x', label='line select')
plt.legend()
plt.title('Lower Maxima')
plt.show()

## Returns 2048 fitted y points
print(len(X), len(Y))
yfitted, params = least_squares_fit.simpfit(X, Y, [1000, 0, 10**5, 0, 0, 0], paramreturn=True)
a, b = least_squares_fit.fit(X, Y, [1000, 0, 10**5, 0, 0, 0], paramreturn=True)
yfitted4, params4 = least_squares_fit.redfit(X, Y, paramreturn=True)
print('simpfit residuals', least_squares_fit.residuals(least_squares_fit.con_sec2, X, Y, params))
print('fit residuals', least_squares_fit.residuals(least_squares_fit.con_sec2, X, Y, b))
print('redfit residuals', least_squares_fit.residuals(least_squares_fit.con_sec3, X, Y, params4), '\n')
print('parameter time!!!')
print(least_squares_fit.param_convert(*params))
print(least_squares_fit.param_convert(*b))
print(least_squares_fit.param_convert(*np.insert(params4, 1, 1)), '\n')

print('Angles')
print(angle(least_squares_fit.param_convert(*params)))
print(angle(least_squares_fit.param_convert(*b)))
print(angle(least_squares_fit.param_convert(*np.insert(params4, 1, 1))), '\n')

yfitted2, params2 = least_squares_fit.simpfit(X2, Y2, [1000, 1, 10**5, 0.1, -100, 0], paramreturn=True)
yfitted3, params3 = least_squares_fit.fit(X2, Y2, [400, 2, 2*10**5, 0.05, -28, 0], paramreturn=True)
yfitted5, params5 = least_squares_fit.redfit(X2, Y2, p0=[10**3, 139000, 0.05, -8.7, 0.00927] ,paramreturn=True)

print('simpfit residuals', least_squares_fit.residuals(least_squares_fit.con_sec2, X2, Y2, params2))
print('fit residuals', least_squares_fit.residuals(least_squares_fit.con_sec2, X2, Y2, params3))
print('redfit residuals', least_squares_fit.residuals(least_squares_fit.con_sec3, X2, Y2, params5), '\n')
print(least_squares_fit.param_convert(*params2))
print(least_squares_fit.param_convert(*params3))

print('\n', 'Angles')
print(angle(least_squares_fit.param_convert(*params2)))
print(angle(least_squares_fit.param_convert(*params3)))

# Plots
plt.plot(x3[0], y3[0], 'x', label='2- all')
plt.plot(X3, Y3, 'x', label='2 - removed')
plt.plot(np.arange(2048), yfitted3, label='2 - fit')
plt.plot(x[0], y[0], 'x', label='1 - all')
plt.plot(X, Y, 'x', label='1 - removed')
plt.plot(np.arange(2048), yfitted4, label='1 - fit')
plt.legend()
plt.show()

dif = yfitted2 - yfitted
print('\n\n\n', dif, '\n')
print(min(dif), '\n', max(dif), '\n')
print('mean: ', sum(dif)/len(dif) )
print('mid-range: ', (max(dif) + min(dif))/2 )
print('partial mean: ', sum(dif[500:len(dif)])/len(dif[500:len(dif)]) )
plt.plot(np.arange(2048), yfitted2 - yfitted, label='simpfit - simpfit')
plt.plot(np.arange(2048), yfitted3 - yfitted, label='fit - simpfit')
plt.legend()
plt.show()
