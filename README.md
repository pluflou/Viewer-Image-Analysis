# Viewer image analysis for SECAR

*Analyzes raw images to extract exact position of the beam beam on the viewer plate.*

### Example outputs:
 ![viewer_example](output/march_beam.gif)
 
## Packages needed

numpy, matplotlib, math,
scikit-image (skimage for io of images, feature detection, peak locating),
lmfit (for fitting beam profiles),
scipy (signal package),
datetime

## How to run

1. Input paths to images and necesary details in INPUT.py
   a. select the image to analyze, with its corresponding background image
   b. if the viewer has been removed from the beamline recently, a new image with the light on might be needed to detect the marked center dots
2. Run with *python3.5 im_analysis.py path/to/tune.tiff*

If you're at the cyclotron lab at MSU:

1. If you're running on an account other than SECAR you might need to install with the --user option (pip install --user package) and run on the *flagtail* node that is running Debian Stretch OS and has python 3.5
2. Code will not work on *fishtank* since that machine runs Python 2.7
3. Make sure to update the paths in the INPUT.py

## How it works

1. In the input file, define the tune image, the background image, and the image of the viewer in position, all taken under the same conditions. The image with the light on is used to find the dots to locate the viewer center by matching a template image of the dots to the light on image. This is not necessary but useful. You first have to specify the region where the dots are in pixels to avoid false positives, and you can refine it or change the number of matches needed in *dot_detection.py*.

2. The code finds the dots matching the dot image and plots the results. If these are not satisfactory you can change the threshold, limits, template, or region before continuing.

3. It subtracts the BG from the raw beam image then integrates the beam profile in x and y. Then it applies a Savitzky-Golay filter to smoothen the data.

4. The point that divides the data in half (median) is calculated and plotted for x and y. This has been chosen based on the fact that the viewer will be used in conjunction with the BCM which centers the beam by dividing it over four quadrants equally and measures the beam intensity in each quadrant. 

5. Optional: The beam profiles can be fitted with the models defined in INPUT.py. Plotting the centers of the gaussians can be instead chosen by commenting out the corresponding lines under each model function in *im_reduction.py*. T
 
## Notes for model fitting

1. A Lorentzian and Voigt model can also be used, among other and any combination thereof. Skewed gaussian and double gaussians have so far been the best fits to recent tunes.
2. The current models have an arbitrary inital guess that might need to be refined in certain cases. 

## To be done in the future

- [ ] Integration with an optimizing routine for automatic tuning
- [ ] Better way of calculating offsets
- [ ] Automatic  detection of peaks and of finding initial guesses for model fitting
- [ ] Optimized fitting routines and selection of best model by comparison of residuals
- [ ] More robust detection of dots on the viewer
