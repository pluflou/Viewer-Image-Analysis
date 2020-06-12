#Viewer Analysis
#Author: Sara Ayoub
#Date: 2/3/2019

from skimage import  io
import sys, os, errno

#make sure bakground, light and beam images have the correct paths
path_to_images= '/home/sara/Documents/SECAR/Diagnostics/Viewer-Image-Analysis/images/june_2020/' #'/mnt/daqtesting/secar_camera/new_captures/'
path_to_code=  '/home/sara/Documents/SECAR/Diagnostics/Viewer-Image-Analysis/' #'/user/e18514/Documents/viewer-image-analysis/'
dir_date= 'optimizer/'
output_path= path_to_code+'output/'+dir_date

raw_image= io.imread(sys.argv[1])
viewer_loc= (sys.argv[2]).capitalize() # i.e. 'D1542'

#Enter here path and name of the background image (make sure it is the SAME SIZE as the tune image)
"""#### Defining settings for each viewer ###"""

bg_im = { 	'D1542': 'D1542_bg_4_4_2020_000.tiff',
			'D1638': 'D1638_bg_4_4_2020_000.tiff',
			'D1688': 'D1688_bg_4_4_2020_000.tiff',
			'D1783': 'D1783_bg_4_4_2020_000.tiff',
			'D1836': 'D1836_bg_4_4_2020_000.tiff',
			'D1879': 'D1879_bg_4_4_2020_000.tiff'
		}

lt_im = { 	'D1542': 'D1542_light_4_4_2020_000.tiff',
			'D1638': 'D1638_light_4_4_2020_000.tiff',
			'D1688': 'D1688_light_4_4_2020_000.tiff',
			'D1783': 'D1783_light_4_4_2020_000.tiff',
			'D1836': 'D1836_light_4_4_2020_000.tiff',
			'D1879': 'D1879_light_4_4_2020_000.tiff'
		}

###### Finding the real center (dots) of the viewer ######
#Define here middle region of viewer in pixels. 
#Refine the region and update center position after seeing matches.

#                ymin, ymax, xmin, xmax
roi = { 'D1515': [200, 320, 630, 870], # not updated
	    'D1542': [40, 120, 40, 120] ,  # updated 5/4/20
		'D1638': [83, 167, 250, 720], # updated 5/4/20
		'D1688': [330, 670, 135, 405], # updated 5/4/20
		'D1783': [178, 536, 308, 926], # updated 5/4/20
		'D1836': [220, 440, 500, 850], #something wrong, updated center location and scale manually 
		'D1879': [230, 370, 230, 360] #something wrong, updated center location and scale manually 

	  }

#                 x, y
cen = { 'D1542': [83, 76], #all updated 6/12/2020
		'D1638': [410, 140],
		'D1688': [276, 494],
		'D1783': [622, 380],
		'D1836': [696, 311],
		'D1879': [285, 294]
	  }	  

#############################################
"""#### ################################# ###"""
#############################################

bg = io.imread(path_to_images + bg_im[viewer_loc])
light_image= io.imread(path_to_images+ lt_im[viewer_loc])

#bg = io.imread('/home/sara/Documents/SECAR/Diagnostics/Viewer-Image-Analysis/images/D1542_2_22_17_34_bg_053.tiff')
#light_image = io.imread('/home/sara/Documents/SECAR/Diagnostics/Viewer-Image-Analysis/images/Light_on_D1542_20190211_final_002.tiff')
y_min, y_max, x_min, x_max = roi[viewer_loc]
viewer_center= cen[viewer_loc]

#Enter here path and name of the image of the viewer dots you wish to use as a template
dotim='/home/sara/Documents/SECAR/Diagnostics/Viewer-Image-Analysis/tiff_files/dots/dot3.tiff'
#'/user/e18514/Documents/viewer-image-analysis/tiff_files/dots/dot3.tiff'
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

