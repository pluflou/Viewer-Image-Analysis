#Viewer Analysis
#Author: Sara Ayoub
#Date: 2/3/2019

from skimage import  io
import sys, os, errno

#make sure bakground, light and beam images have the correct paths
path_to_images= '/mnt/daqtesting/secar_camera/new_captures/'
path_to_code=  '/user/e18514/Documents/viewer-image-analysis/'
dir_date= 'optimizer/'
output_path= path_to_code+'output/'+dir_date

raw_image= io.imread(sys.argv[1])
viewer_loc= sys.argv[2] # i.e. 'D1542'

#Enter here path and name of the background image (make sure it is the SAME SIZE as the tune image)
"""#### Defining settings for each viewer ###"""

bg_im = { 	'D1542': 'D1542_BG_03-093_000.tiff'
			'D1568':
		}

lt_im = {   'D1542': 'D1542_03-07_light_image_000.tiff'
			'D1568':
		}

###### Finding the real center (dots) of the viewer ######
#Define here middle region of viewer in pixels. It helps to look at the image first and then refine the region after seeing matches.

cen = { 'D1542': [100, 85] #updated 9/16/2019
		'D1568': [296+5, 150+5]
	  }

roi = { 'D1515': [200, 320, 630, 870]
	    'D1542': [40, 140, 60, 160]   # updated 4/9/19
		'D1568': [81, 229, 214, 382]
	  }

#############################################
"""#### ################################# ###"""
#############################################

bg = io.imread(path_to_images + bg_im[viewer_loc])
light_image= io.imread(path_to_images+ lt_im[viewer_loc])

y_min, y_max, x_min, x_max = roi[viewer_loc]
viewer_center= cen[viewer_loc]

#Enter here path and name of the image of the viewer dots you wish to use as a template
dotim= '/user/e18514/Documents/viewer-image-analysis/tiff_files/dots/dot3.tiff'
template= io.imread(dotim) 

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

