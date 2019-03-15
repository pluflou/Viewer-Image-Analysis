#Viewer Analysis
#Author: Sara Ayoub
#Date: 2/3/2019

from skimage import  io
import sys

#Enter here the images and the methods that will be used for the viewer analysis
#Make sure to inlcude the path to the images

###### Image reduction ########
#Enter here path and name of the tune image
raw_image= io.imread(sys.argv[1])
#raw_image= io.imread('tiff_files/Tune115_07722018_viewer_D1542_001.tiff')

#Enter here path and name of the background image (make sure it is the SAME SIZE as the tune image)
bg= io.imread('images/D1542_images/D1542_bg_3_11_8pm_057.tiff')
#bg= io.imread('/user/secaruser/Documents/viewer_images/vd-d1542/Background_D1542_20190212_final_003.tiff')

###### Finding the real center (dots) of the viewer ######
#Enter here path and name of the image of the viewer with light on. 
#Make sure it is compatible (same size and taken at the same time) with tune!
#light_image= io.imread('tiff_files/180720_D1542_S20_2_003.tiff')
light_image= io.imread('images/D1542_images/D1542_lighton_3_11_063.tiff')

#Define here middle region of viewer in pixels
#It helps to look at the image first and then refine the region after seeing matches
y_min= 50 #vertical axis in image
y_max= 120
x_min= 50 #horizontal axis in image
x_max= 120

#Enter here path and name of the image of the viewer dots you wish to use as a template
template= io.imread('tiff_files/dots/dot3.tiff') #dot2 seems good

#Enter here the threshold (minimum intensity of peaks) to detect dots on image
#Don't change this at the beginning. It is better to have a good search region first
threshold= 0.002

###### Fitting beam profiles ##########
#Use these as default first then decide after looking at profiles if another model is a better fit
#Options are: single_gaussian, double_gaussian, skewed_gaussian, gaussian_skewed_gaussian
y_profile_model= 'double_gaussian'
x_profile_model= 'skewed_gaussian'



