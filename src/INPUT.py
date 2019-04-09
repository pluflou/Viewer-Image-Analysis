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
bg= io.imread('/mnt/daqtesting/secar_camera/new_captures/April_5/D1542/D1542_4_5_1pm_bg_127.tiff')
#bg= io.imread('/home/sara/Documents/SECAR/Diagnostics/Viewer-Image-Analysis/images/3_25_images/E25_1/D1542_3_25_bg_10_pm_068.tiff')



###### Finding the real center (dots) of the viewer ######
#Enter here path and name of the image of the viewer with light on. 
#Make sure it is compatible (same size and taken at the same time) with tune!
#light_image= io.imread('/mnt/daqtesting/secar_camera/new_captures/vd-d1515/D1515_lighton_3_6_adjusted_027.tif')
#light_image= io.imread('../tiff_files/180720_D1542_S20_2_003.tiff')
light_image= io.imread('/mnt/daqtesting/secar_camera/new_captures/April_4/D1542/D1542_4_4_5pm_lighton_115.tiff')
#light_image= io.imread('/home/sara/Documents/SECAR/Diagnostics/Viewer-Image-Analysis/images/3_25_images/E25_1/D1515_lightOn_3_25_2pm_033.tif')

#Define here middle region of viewer in pixels
#It helps to look at the image first and then refine the region after seeing matches

##D1515##
#y_min= 200 #vertical axis in image
#y_max= 320
#x_min= 630 #horizontal axis in image
#x_max= 870

##D1542##
y_min= 70 #vertical axis in image
y_max= 120
x_min= 120 #horizontal axis in image
x_max= 189

d1542_center= [84, 82] #x,y -- update this when viewer moves in the screen

#Enter here path and name of the image of the viewer dots you wish to use as a template
template= io.imread('/user/secaruser/Documents/Viewer-Image-Analysis/tiff_files/dots/dot3.tiff') #dot2 seems good
#template= io.imread('/home/sara/Documents/SECAR/Diagnostics/Viewer-Image-Analysis/tiff_files/dots/dot4.tiff') #dot2 seems good

#Enter here the threshold (minimum intensity of peaks) to detect dots on image
#Don't change this at the beginning. It is better to have a good search region first
threshold= 0.1


###### Fitting beam profiles ##########
#Use these as default first then decide after looking at profiles if another model is a better fit
#Options are: single_gaussian, double_gaussian, skewed_gaussian, gaussian_skewed_gaussian
y_profile_model= 'double_gaussian'
x_profile_model= 'skewed_gaussian'



