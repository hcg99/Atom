import numpy as np
import matplotlib.pyplot as plt
import h5py
import itertools
from scipy.stats import logistic
import array as arr

# Define variables
pedestal_mean = 60
dim = 2048
sub_data = []

# Pedestal subtraction function
def pedestal_subtraction(pedestal_mean, data_in):
    for i in range(20):
        data_in[i] = data_in[i].astype('float64')
        data_in[i] -= pedestal_mean
    return data_in

## Play around with ADU values to get clear picture
def picture_play(data):
    for i in range(dim):
        for j in range(dim):
            if data[i][j] < 0:
                data[i][j] = 60000
    return data

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

sub_data = pedestal_subtraction(pedestal_mean, image_data)

play_data = picture_play(image_data[8])

for k in range(1):
# Plot a good dataset - here index 8 (but there are others too!)
    plt.imshow(play_data)
    plt.show()

# The histogram of the data will help show possible single photon hits
    #plt.hist(sub_data[8].flatten(), bins=100)
    #plt.yscale('log')
    #plt.show()
    #plt.hist(image_data2[8].flatten(), bins=100)
    #plt.yscale('log')
    #plt.show()
