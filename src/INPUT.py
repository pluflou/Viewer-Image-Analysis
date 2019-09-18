#Viewer Analysis
#Author: Sara Ayoub
#Date: 2/3/2019

from skimage import  io
import sys, os, errno

path_to_images= '/mnt/daqtesting/secar_camera/new_captures/'
path_to_code=  '~/Documents/Viewer-Image-Analysis/' # '/user/secaruser/Documents/Viewer-Image-Analysis/'
dir_date= 'optimizer/'
viewer_loc= 'D1542'
output_path= path_to_code+'output/'+dir_date

show_plots= False
		
#Enter here the images and the methods that will be used for the viewer analysis
#Make sure to inlcude the path to the images

###### Image reduction ########
#Enter here path and name of the tune image
raw_image= io.imread(sys.argv[1])

#Enter here path and name of the background image (make sure it is the SAME SIZE as the tune image)
bg= io.imread(path_to_images + 'light_bg/D1542_9_12_dipole_scan_bg_001.tiff')

###### Finding the real center (dots) of the viewer ######
#Path to updated/compatible image of the viewer with light on. 
light_image= io.imread(path_to_images+'light_bg/D1542_9_12_dipole_scan_lighton_001.tiff')

#Define here middle region of viewer in pixels. It helps to look at the image first and then refine the region after seeing matches.

##D1515##
#y_min= 200 #vertical axis in image
#y_max= 320
#x_min= 630 #horizontal axis in image
#x_max= 870

##D1542## updated 4/9/19
y_min= 100 #vertical axis in image
y_max= 250
x_min= 90 #horizontal axis in image
x_max= 550

#d1542_center= [163, 93] #x,y -- update this when viewer moves in the screen
d1542_center= [207, 177] #updated 9/16/2019

#Enter here path and name of the image of the viewer dots you wish to use as a template
template= io.imread(path_to_code+'tiff_files/dots/dot3.tiff') #dot2 seems good

#Enter here the threshold (minimum intensity of peaks) to detect dots on image
#Don't change this at the beginning. It is better to have a good search region first
threshold= 0.1

##### function to create path to output if dir was not created before
def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc:
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise

###### Fitting beam profiles ##########
#Use these as default first then decide after looking at profiles if another model is a better fit
#Options are: single_gaussian, double_gaussian, skewed_gaussian, gaussian_skewed_gaussian
y_profile_model= 'double_gaussian'
x_profile_model= 'skewed_gaussian'

