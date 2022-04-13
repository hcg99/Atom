import numpy as np
import matplotlib.pyplot as plt
import h5py
import itertools
from scipy.stats import logistic

# Define variables
pedestal_mean = 60
dim = 2048
sub_data = []

# Pedestal subtraction function
def pedestal_subtraction(pedestal_mean, data_in_):
    data_in = data_in_.copy()
    for i in range(20):
        data_in[i] = data_in[i].astype('float64')
        data_in[i] -= pedestal_mean[i]
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
                        ## keep centre of island at -60000 until end of loop to brevent erroneous breaking
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

## The histogram of the data will help show possible single photon hits
## Accepts only 1 image
def hist(data, bins=100, title=''):
    plt.hist(data.flatten(), bins=bins, log = True)
    #plt.yscale('log')
    plt.title(title)
    plt.show()
    #plt.hist(image_data2[8].flatten(), bins=100)
    #plt.yscale('log')
    #plt.show()

## Plots images; accepts multi-image input
def plot1D(data, x = [], title = 'Hello', xlabel='x', ylabel='y', style='b-' ):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if len(x) == 0:
        plt.plot(data)
    else:
        plt.plot(x, data, style)
    #plt.yscale('log')
    plt.title(title)
    plt.show()

def plot2D(data, title = 'Hello', xlabel='x', ylabel='y', style='b-' ):
    #print(type(data))
    if type(data[0]) != np.ndarray and type(data[0]) != list:
        #print('1')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if len(x) == 0:
            plt.plot(data)
        else:
            plt.plot(x, data, style)
        #plt.yscale('log')
        plt.title(title)
        plt.show()
    elif type(data[0][0]) != np.ndarray and type(data[0][0]) != list:
        #print('2')
        plt.imshow(data)
        plt.title(title)
        plt.show()
    else:
        #print('3')
        for k in range(len(data)):
            plt.imshow(data[k])
            plt.title(k)
            plt.show()

## summs ADU of multiple images to make spectral lines clearer
## inputs: list of image arrays; list of indexes of the images selected for the sum
def sum(data_, *index):
    if len(index) == 0:
        index = list(range(len(data_)))
        print('Data Sum: no index argument so all data will be summed')
    else:
        index = list(index)[0]

    data_in = data_.copy()
    data_out = data_in[index[0]].copy()
    index.pop(0)

    for i in index:
        data_out += data_in[i]

    return data_out

##Input: 1 set of data
##Output: Modal ADU value
def ped_peak(data):
    if len(data) == dim:
        [binVal, binEdg] = plt.hist(data.flatten(), bins=100, log=True)[:2]
        #plt.show()
        binVal = list(binVal)
        index = binVal.index((max(binVal)))
        peakPos = (binEdg[index] + binEdg[index + 1])/2
        plt.close()
        return peakPos

    ## for many input images:
    peakPos = []
    iter = range(len(data))
    for i in iter:
        [binVal, binEdg] = plt.hist(data[i].flatten(), bins=100, log=True)[:2]
        binVal = list(binVal)
        index = binVal.index((max(binVal)))
        peakPos.append((binEdg[index] + binEdg[index + 1])/2)
        plt.close()
    return peakPos


#image_data = UI.function()

#sub_data = pedestal_subtraction(pedestal_mean, image_data)

#spes = 16
good = [1,2,4,6,7,8,11,14,16,17,19]
bad = [0,3,5,9,10,12,13,15,18]

#sum_data = sum(sub_data, good)
#print(len(sum_data))

#play_data = [picture_play(sum_data), picture_play2(sum_data)]
#play_data = [picture_play(sub_data[spes]), picture_play2(sub_data[spes])]

#plot(sum_data)
#plot(play_data)
#hist(image_data[spes])
