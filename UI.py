import numpy as np
import matplotlib.pyplot as plt
import h5py
import itertools
from scipy.stats import logistic
import array as arr

## Takes an hdf data file; returns all the images in the file; prints the number of images
## If called with an integer index, single image at given index is returned  
def function(index = []):
    # Name of the hdf file that contain the data we need
    f_name = 'sxro6416-r0504.h5'

    # Open the hdf5 file, use the path to the images to extrate the data and place
    # it in the image data object for further manipulation and inspection.
    datafile = h5py.File(f_name, 'r')

    # Allow for quick extraction of 1 image
    if index != []:
        return datafile.get(f'Configure:0000/Run:0000/CalibCycle:{index:04d}/Princeton::FrameV2/SxrEndstation.0:Princeton.0/data')[0]

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

    return image_data
