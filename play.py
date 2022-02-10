import numpy as np
import matplotlib.pyplot as plt
import h5py
import itertools
from scipy.stats import logistic


# Name of the hdf file that contain the data we need
f_name = 'sxro6416-r0504.h5'

# Open the hdf5 file, use the path to the images to extrate the data and place
# it in the image data object for further manipulation and inspection.
datafile = h5py.File(f_name, 'r')
image_data = []
for i in itertools.count(start=0):
    d = datafile.get(f'Configure:0000/Run:0000/CalibCycle:{i:04d}/Princeton::FrameV2/SxrEndstation.0:Princeton.0/data')
    if d is not None:
        # actual image is at first index
        image_data.append(d[0])
    else:
        break

# Tell me how many images were contained in the datafile
print(f"loaded {len(image_data)} images")


# Plot a good dataset - here index 8 (but there are others too!)
image_fraction = []

## display a small section of the image so we might actually see the data
#for i in range(100):
    #image_fraction[i] = image_data[8][i][0:99]
    #image_fraction.append(image_data[8][i][0:99])
#print(f"loaded {len(image_fraction)} images")
#print(image_fraction)
#plt.imshow(image_fraction)
#plt.show()



#x = image_data[8].flatten()
#for j in range(4194304):
#    if x[j] < 50:
#        count += 1
#print(count)

#image_summed = image_data[19]
#for i in range(19):
#     image_summed += image_data[i]
#
#image_summed = image_summed/20

#plt.imshow(image_summed)
#plt.show()

## count number of pixels obeying certain criteria

def function_pos():
    positions = []
    count = [0]
    spread_cnt = [0, 0, 0, 0]
    for k in range(1):
        k = 4
        spillage = 0
        image_swept = image_data[k]
        count.append(0)
        for i in range(2048):
            for j in range(2048):
                if image_swept[i][j] > 130:
                    positions.append([i,j])
                    bool = -1
                    for I in range(2):
                        for J in range(2):
                            if image_swept[i+I-1][j+J-1] > 100:
                                spillage += 1
                                bool += 1
                    match bool:
                        case 0:
                            spread_cnt[0] += 1
                        case 1:
                            spread_cnt[1] += 1
                        case 2:
                            spread_cnt[2] += 1
                        case 3:
                            spread_cnt[3] += 1
                    count[0] += 1
    return positions, spillage, count, spread_cnt

pos = function_pos()[0]
spillage = function_pos()[1]
count = function_pos()[2]
spread_cnt = function_pos()[3]
print(count)
#print(spillage)
print(spillage - count[0])
print(spread_cnt)

## plot the data
#plt.imshow(image_swept)
#plt.show()

## The histogram of the data will help show possible single photon hits
#plt.hist(image_swept.flatten(), bins=100)
#plt.yscale('log')
#plt.show()

input('press enter to exit')
