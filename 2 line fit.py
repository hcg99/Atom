import numpy as np
import matplotlib.pyplot as plt
import h5py
import itertools
from scipy.stats import logistic
import array as arr
import UI

# Define variables
pedestal_mean = 60
dim = 2048
sub_data = []

# Pedestal subtraction function
def pedestal_subtraction(pedestal_mean, data_in_):
    data_in = data_in_.copy()
    for i in range(20):
        data_in[i] = data_in[i].astype('float64')
        data_in[i] -= pedestal_mean
    return data_in

## The histogram of the data will help show possible single photon hits
## Accepts only 1 image
def hist(data):
    plt.hist(data.flatten(), bins=100, log = True)
    #plt.yscale('log')
    plt.show()
    #plt.hist(image_data2[8].flatten(), bins=100)
    #plt.yscale('log')
    #plt.show()

## Plots images; accepts multi-image input;
def plot(data, title):
    if len(data) == 2048:
        plt.imshow(data)
        plt.title(title)
        plt.show()
    else:
        for k in range(len(data)):
            plt.imshow(data[k])
            plt.title(k)
            plt.show()

## Takes a sqaure of data size len x len and sums pixel values. Repeats over all squares in the data
## Returns the position of square with the maximum sum
## Inputs: data; number of pixels per sum; number of peaks per row; x_min; x_max; bool sum continuously or discretely
## we expect right line to be 1400 < x < 1500 & left line 1250 < x < 1350
def find_peaks(data_, len, num_max, x_min, x_max, cont):
    data = data_.copy()
    output = data.copy()*0
    step = 1

    ## i runs through the rows
    for i in range(0, dim - len + 1, len):
        ## max is [maximum peak sum, [peak position]]
        max_val = [0.0]*num_max
        max_pos = [0]*num_max
        #print(max_val, max_pos)
        if cont == False:
            step = len
        ## j runs across the colums
        for j in range(len + x_min, x_max - len + 1, step):
            sum = 0
            for l in range(len):
                for l_ in range(len):
                    sum += data[i+l_][j+l]

            for k in range(num_max):
                if sum > max_val[k]:
                    if k != num_max - 1:
                        continue
                    k = k + 1
                elif k < 1:
                    break
                #max_val = np.delete(max_val, 0)
                max_val.pop(0)
                max_pos.pop(0)
                #max_val = np.insert(max_val, k-1, sum.copy())
                max_val.insert(k-1, sum.copy())
                max_pos.insert(k-1, [i + round(len/2), j])
                break
        #print(max)
        #print(max_pos[1][1], max_pos[0][1])
        for k in range(num_max):
            for l in range(len):
                for l_ in range(len):
                    ## make highest squares show up on the image
                    #print(l_)
                    #print(output[i+l_][max_pos[k][1]+l], max_pos[k][1])
                    #print(l_)
                    output[i+l_][max_pos[k][1]+l] = k + 1

    return output


image_data = UI.function()

spes = 8
good = [1,2,4,6,7,8,11,14,16,17,19]
bad = [0,3,5,9,10,12,13,15,18]

line_data = find_peaks(image_data[spes], 16, 4, 0, 2048, False)
plot(line_data, 'cont. full square sum')
