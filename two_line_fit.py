import numpy as np
from scipy.stats import logistic

# Define variables
dim = 2048

## Takes a sqaure of data size len x len and sums pixel values. Repeats over all squares in the data
## Returns the position of squares with the maximum sum
## Inputs: data; number of pixels per sum; number of peaks per row; x_min; x_max; bool sum continuously or discretely
## Outputs: output; array same size as the input data, mostly zeros but higher values at the highest sum squares
##          out_posX; list of 1D lists containing row position (y value) of each of the highest squares (positions are evenly spaced)
##          out_posY; list of 1D lists containing column position (x value) of each of the highest squares
## we expect right line to be 1400 < x < 1530 & left line 1250 < x < 1380
def find_peaks(data_, len, num_max, x_min, x_max, cont, square):
    data = data_.copy()
    output = data.copy()*0
    out_posX = [[]]*num_max
    out_posY = [[]]*num_max

    ## step determines continuous or discrete summing
    step = 1
    if cont == False:
        step = len
    ## len_ is width of squares
    len_ = len
    if square == False:
        len_ = 1

    ## i runs through the rows
    for i in range(0, dim - len + 1, len):
        ## max is [maximum peak sum, [peak position]]
        max_val = [0.0]*num_max
        max_pos = [0]*num_max

        ## j runs across the colums
        for j in range(x_min, x_max - len_ + 1, step):
            ## takes a rectangular selection of points and sums adu values
            sum = 0

            for l in range(len):
                for l_ in range(len_):
                    sum += data[i+l][j+l_]

            ## looks at the sum of adu values and adds it to a list of the max values if its big enough
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

        ## makes squares of non-zero value in our output at locations of highest sum
        for k in range(num_max):
            ## creates array of positions of points
            out_posX[k].append(max_pos[k][0])
            out_posY[k].append(max_pos[k][1] + round(len/2))
            for l in range(len):
                ## draw lines at x_min & x_max
                output[i+l][x_min] = num_max
                output[i+l][x_max] = num_max
                for l_ in range(len_):
                    # in each row, value of the highest square is not uniform
                    output[i+l][max_pos[k][1]+l_] = k + 1

    return output, out_posX, out_posY
