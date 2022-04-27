READ.ME





To produce the X-ray emission spectrum, run the file "spectrum.py"
There is a variable in this file called "index" which selects
which image out of the 20 provided gets examined.





bremsstrahlung.py
    creates bremsstrahlung spectrum + L series peaks

curve_fit.py
    old version of least_squares_fit

Energy_assign.py
    takes inputs of alpha and the 2 fitted spectral line's positions and separations
    outputs the Energy Matrix - a 2048 by 2048 square matrix of photon energy at each CCD pixel

Experiment.py
    python file to mess around with syntax

genericFilter.py
    module to explore creating a photon counting algorithm
    used to find optimum values for thresholding and error calculation

getFits.py
    calls least_squares_fit & two_line_fit to output arrays
    of 2048 y values for the 2 spectral peaks and mean distance between peaks

least_squares_fit.py
    scipy fits a conic section to input data

main.py
    a collection of useful functions:
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

optimizeAlpha.py
    uses inputs of the two fitted spectral lines to produce an optimized value
    for alpha, than angle between the normals to the CCD and the crystal diffraction
    plane

play.py
    investigate ADU properties to shed light on single photon counting

singlePhotonCount.py
    estimates the location of photon events within an input data set and provides
    values for the uncertainty on photon number

spectrum.py
    calls many modules to produce the x-ray emission spectrums

tester.py
    contains some of the same functions as main.py

two_line_fit.py
    finds highest value ADU rectangles in the data to hopefully identify spectral lines

UI.py
    extracts image data from the data file






pickle:
  data
    sum of all non-dark data sets
  databad
    sum of all dark data sets
  Emat
    matrix of energy for its corresponding pixel: energies at spectral peaks are 20 eV larger than expected
  Emat2
    matrix of energy for its corresponding pixel
  phoE
    list of photon energies
  SynData
    synthetic data
  SynPos
    matrix of zeros with 1s and 2s at photon event locations for SynData
  PhoPos(6)
    positions (0,1,2) of photons in data set 6

E = 1188.0, 1215.5

Spectrum - makes x ray spectrum
Energy_assign - makes photon energy matrix (calls getFits to fit spectral peaks)
genericFilter - photon counting
module1 - creates synthetic data
