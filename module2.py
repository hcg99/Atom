import numpy as np
import main
import UI
import two_line_fit
import tester
import least_squares_fit

import matplotlib.pyplot as plt

image_data = UI.function()

sum_data = main.sum(image_data)

line_data = []
## two_line_fit.find_peaks()
## Inputs: data; square size; number of squares per row; x_min; x_max; continuous True or False; square True or False
## Outputs: [full size grid of 0s with sqaures at higest ADU areas, 2D list of each squares' row, 2D list of each squares' column]
line_data.append( two_line_fit.find_peaks(sum_data, 32, 1, 1230, 1390, True, True) )
line_data.append( two_line_fit.find_peaks(sum_data, 32, 1, 1380, 1550, True, True) )

line1 = np.array(line_data[0][0])
line2 = np.array(line_data[1][0])
xdata1 = np.array(line_data[0][1][0])
xdata2 = np.array(line_data[1][1][0])
ydata1 = np.array(line_data[0][2][0])
ydata2 = np.array(line_data[1][2][0])
data = line1 + line2

#fitdata1 = least_squares_fit.fit(xdata1, ydata1)
fitdata2 = least_squares_fit.fit(xdata2, ydata2)

## add the fitted line on top of our squares data
lin = np.zeros((main.dim, main.dim))
for i in range(main.dim):
    lin[i][round(fitdata2[i])] = -1000

main.plot2D(sum_data, 'sum data')
enhanced_image = np.array( main.picture_play( main.sum(main.pedestal_subtraction(main.ped_peak(image_data), image_data), main.good) ) )
print(len(enhanced_image))
print(len(enhanced_image[0]))

plt.imshow(enhanced_image)
plt.show()

print(lin)
print(enhanced_image)

main.plot2D(enhanced_image, 'enhanced sum data')

for i in range(main.dim):
    enhanced_image[i][round(fitdata2[i])] = -1000


print(enhanced_image)

main.plot2D(enhanced_image, '2 lines')
