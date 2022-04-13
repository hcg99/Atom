READ.ME

bremsstrahlung.py
    creates bremsstrahlung spectrum + L series peaks

curve_fit.py
    old version of least_squares_fit

Experiment.py
    python file to mess around with syntax

least_squares_fit.py
    scipy fits a conic section to input data

main.py
    a bunch of useful functions:
        pedestal subtraction; find peak of a histogram; plot 1D, 2D and hist; picture_play to enhance images; sum data

model_data.py
    used to find pedestal peaks over 20 images

module1.py
    creates synthetic photon events
    calls bremsstrahlung

module2.py
    fits lines on real data and plots the line on an enhanced image of the data
    calls least_squares_fit & two_line_fit

module3.py
    calls two_line_fit to obtain points close to the spectral peaks
    removes anomalous points
    calls least_squares_fit to fit the line

play.py
    investigate ADU properties to shed light on single photon counting

Round.py
    rounds numbers correctly

tester.py
    contains some of the same functions as main.py

two_line_fit.py
    finds highest value ADU rectangles in the data to hopefully identify spectral lines

UI.py
    extracts image data from the data file

Energy_assign.py
    creates energy matrix

getFits.py
    calls l_s_f & t_l_f to output arrays of 2048 y values for the 2 spectral peaks and mean distance between peaks

genericFilter.py
    photon counting

  
pickle:
  data
    sum of all non-dark data sets
  Emat
    matrix of energy for its corresponding pixel
  phoE
    list of photon energies
