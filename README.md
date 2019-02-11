##Viewer image analysis for SECAR program 

#Packages needed:
numpy, matplotlib, math
scikit-image (skimage for io of images, feature detection, peak locating)
lmfit (for fitting beam profiles)
scipy (signal package)

#How to run:
1. *ssh -X secaruser@flagtail* (code will not work with the python version on fishtank)
1. Input paths to images and necesary details in INPUT.py
2. Run with *python3.5 im_analysis.py path/to/tune.tiff*

#How it works

1. In the input file, define the tune image, the background image, and the image of the viewer in position, all taken under the same conditions. The image with the light on is used to find the dots to locate the viewer center. This is not necessary but useful. You first have to specify the region where the dots are in pixels to avoid false positives, and you can refine it or change the number of matches needed in *dot_detection.py*.

2. The code finds the dots matching the dot image and plots the results. If these are not satisfactory you can change the threshold, limits, template, or region before continuing.

3. It subtracts the BG then integrates the beam profile in x and y. Then it applies a Savitzky-Golay filter to smoothen the data.

4. The beam profiles are fitted with the models defined in INPUT.py. The point that divides the data in half (median) is calculated and plotted for x and y. This has been chosen based on the fact that the viewer will be used in conjunction with the BCM which centers the beam by dividing it over four quadrants equally. Plotting the centers of the gaussians can be instead chosen by commenting out the corresponding lines under each model function in *im_reduction.py*.
 
#Notes
1. A Lorentzian and Voigt model can also be used, among other and any combination thereof. Skewed gaussian and double gaussians have so far describes most tunes best.
2. The current models have an arbitrary inital guess that might need to be refined in certain cases. 
3. If you're running on an account other than SECAR you might need to install with the --user option (pip install --user package) and run on the *flagtail* node that is running Debian Stretch OS and has python 3.5

#To be done in the future:
1. Better way of calculating offsets.
2. Automatic  detection of peaks and of finding initial guesses for model fitting.
3. Optimized fitting routines and selection of best model by comparison of residuals.
4. More robust detection of dots on the viewer.
