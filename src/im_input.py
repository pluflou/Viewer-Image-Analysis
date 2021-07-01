#Viewer Analysis
#Author: Sara Ayoub
#Date: 2/3/2019

import skimage.io as io 
import sys, os, errno

import settings

# setting the correct paths
path_to_images = settings.im_path
path_to_code =  '/user/e18514/Documents/viewer-image-analysis/'
dir_date = 'optimizer/'
output_path = path_to_code+'output/'+dir_date

raw_image = io.imread(sys.argv[1])
viewer_loc = (sys.argv[2]).capitalize() # e.g. 'D1542'

# BG image import
bg = io.imread(settings.bg_path + settings.bg_im[viewer_loc])

# Viewer ROI with center and dots
y_min, y_max, x_min, x_max = settings.roi[viewer_loc]
viewer_center= settings.cen[viewer_loc]

# setting conversion
scale = settings.scale_dict[viewer_loc]
px_to_mm = 5/scale

# recreating the correct dots on viewer to plot
viewer_dots=[[viewer_center[0],viewer_center[0],viewer_center[0], viewer_center[0]+ scale, 
            viewer_center[0]- scale],
[viewer_center[1]+scale,viewer_center[1]-scale,viewer_center[1],viewer_center[1],viewer_center[1]]]

# function to create path to output if dir was not created before
def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc:
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise

