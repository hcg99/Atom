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

## Play around with ADU values to get clear picture
def picture_play(data_):
    data = data_.copy()
    for i in range(dim):
        for j in range(dim):
            ## creates 3x3 islands of high value on pixels with ADU over 50
            if data[i][j] > 60:
                for I in range(3):
                    for J in range(3):
                        ## break to stop program thinking edges of islands are pixels with ADU over 50
                        if data[i][j] == 60000:
                            break
                        ## accounts for islands not being able to spill out of the 2048^2 frame
                        elif i+I-1 < 2048 and i+I-1 > -1 and j+J-1 < 2048 and j+J-1 > -1:
                            data[i+I-1][j+J-1] = 60000
                        ## keep centre of island at -60000 until end of loop to brevent brevoneous breaking
                        data[i][j] = -60000
                data[i][j] = 60000
            ## create 1x1 island of medium value on pixel with 20 < ADU < 50
            elif data[i][j] > 20:
                data[i][j] = 30000

    return data

def picture_play2(data_):
    data = data_.copy()
    for i in range(dim):
        for j in range(dim):
            if data[i][j] < 0:
                data[i][j] = -60000
            else:
                data[i][j] = 60000
    return data

## Play around with ADU values to get thresholds
def picture_play(data_):
    data = data_.copy()
    for i in range(dim):
        for j in range(dim):
            ## creates 3x3 islands of high value on pixels with ADU over 50
            if data[i][j] > 60:
                for I in range(3):
                    for J in range(3):
                        ## break to stop program thinking edges of islands are pixels with ADU over 50
                        if data[i][j] == 60000:
                            break
                        ## accounts for islands not being able to spill out of the 2048^2 frame
                        elif i+I-1 < 2048 and i+I-1 > -1 and j+J-1 < 2048 and j+J-1 > -1:
                            data[i+I-1][j+J-1] = 60000
                        ## keep centre of island at -60000 until end of loop to brevent brevoneous breaking
                        data[i][j] = -60000
                data[i][j] = 60000
            ## create 1x1 island of medium value on pixel with 20 < ADU < 50
            elif data[i][j] > 20:
                data[i][j] = 30000

    return data

## The histogram of the data will help show possible single photon hits
## Accepts only 1 image
def hist(data):
    plt.hist(data.flatten(), bins=100, log = True)
    #plt.yscale('log')
    plt.show()
    #plt.hist(image_data2[8].flatten(), bins=100)
    #plt.yscale('log')
    #plt.show()

## Plots images; accepts multi-image input
def plot(data, title='hello'):
    if type(data) == np.ndarray:
        plt.imshow(data)
        plt.title(title)
        plt.show()
    else:
        for k in range(len(data)):
            plt.imshow(data[k])
            plt.title(k)
            plt.show()

## summs ADU of multiple images to make spectral lines clearer
## inputs: list of image arrays; list of indexes of the images selected for the sum
def sum(data_, index):
    data_in = data_.copy()
    data_out = data_in[index[0]].copy()
    index.pop(0)

    for i in index:
        data_out += data_in[i]

    return data_out

def section_select(data, xmin, xmax, ymin, ymax):
    plot(data[ymin:ymax, xmin:xmax], 'data section')

def self_function():
    image_data = UI.function()

    sub_data = pedestal_subtraction(pedestal_mean, image_data)

    spes = 16
    good = [1,2,4,6,7,8,11,14,16,17,19]
    bad = [0,3,5,9,10,12,13,15,18]

    sum_data = sum(sub_data, good)

    section_select(image_data[spes], 1754, 1761, 1392, 1399)
    plot(sum_data)
    hist(image_data[11])
    hist(sum_data)

    play_data = [picture_play(sum_data), picture_play2(sum_data)]
    #play_data = [picture_play(sub_data[spes]), picture_play2(sub_data[spes])]

    #plot(sum_data)
    plot(play_data)
    #hist(image_data[spes])

self_function()
