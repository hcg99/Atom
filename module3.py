import numpy as np
import two_line_fit
import UI
import main
import matplotlib.pyplot as plt
import least_squares_fit

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


plt.plot(x2[0], y2[0], 'x', label='square')
plt.plot(x3[0], y3[0], 'x', label='line')

X, Y = point_select(x[0], y[0])
X2, Y2 = point_select(x2[0], y2[0])
X3, Y3 = point_select(x3[0], y3[0])

plt.plot(X2, Y2, 'x', label='sqare select')
plt.plot(X3, Y3, 'x', label='line select')
plt.legend()
plt.show()

plt.plot(X3, Y3, 'x', label='line select')
plt.legend()
plt.show()

## Returns 2048 fitted y points
print(len(X), len(Y))
yfitted, params = least_squares_fit.simpfit(X, Y, [1000, 0, 10**5, 0, 0, 0], paramreturn=True)
yfitted2, params2 = least_squares_fit.simpfit(X2, Y2, [1000, 1, 10**5, 0.1, -100, 0], paramreturn=True)
yfitted3 = least_squares_fit.fit(X3, Y3, [400, 2, 2*10**5, 0.05, -28, 0])

print('parameter time!!!')
print(params)
print(params2)

# Plots
plt.plot(x3[0], y3[0], 'x', label='2- all')
plt.plot(X3, Y3, 'x', label='2 - removed')
plt.plot(np.arange(2048), yfitted3, label='2 - fit')
plt.plot(x[0], y[0], 'x', label='1 - all')
plt.plot(X, Y, 'x', label='1 - removed')
plt.plot(np.arange(2048), yfitted, label='1 - fit')
plt.legend()
plt.show()
