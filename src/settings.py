# Settings for viewer configuration

# Show each analysis visual plot when running?
# Set to False when using with the beam_optimizer unless debugging
show_plots = False

# Path to image storage
im_path = '/mnt/daqtesting/secar_camera/new_captures/'
bg_path = im_path + 'lighton_and_background/' 

# Enter here name of the background image
# SAVE THIS IMAGE TO lighton_and_background/ in the mnt/ images folder
bg_im = { #'D1542': 'D1542_BG_07-27_23:12_000.tiff',
          'D1542': 'D1542_bg_07-20_16:13_000.tiff',
          'D1638': 'D1638_bg_7_1_gain40_e1_2_000.tiff',
	  #'D1638': 'D1638_bg_7_28_2020_000.tiff',
	  'D1688': 'D1688_bg_7_28_2020_000.tiff',
	  'D1783': 'D1783_bg_07_30_3_19_000.tiff',
	  'D1836': 'D1836_bg_7_29_12_44_000.tiff',
	  'D1879': 'D1879_BG_07-30_00:59_000.tiff'
		}
# Enter here name of the image with the light on
# SAVE THIS IMAGE TO lighton_and_background/ in the mnt/ images folder
lt_im = { 	'D1542': 'D1542_light_4_4_2020_000.tiff',
		'D1638': 'D1638_light_4_4_2020_000.tiff',
		'D1688': 'D1688_light_4_4_2020_000.tiff',
		'D1783': 'D1783_light_4_4_2020_000.tiff',
		'D1836': 'D1836_light_4_4_2020_000.tiff',
		'D1879': 'D1879_light_4_4_2020_000.tiff'
		}

# Finding the real center (dots) of the viewer
# These can be foud easily using dot_detection.py
# Define here middle region of viewer in pixels 
#                ymin, ymax, xmin, xmax
roi = { 'D1515': [200, 320, 630, 870], # not updated
	'D1542': [40, 120, 40, 120] ,  # updated 5/4/20
	'D1638': [83, 167, 250, 720],  # updated 5/4/20
        'D1688': [330, 670, 135, 405], # updated 5/4/20
	'D1783': [178, 536, 308, 926], # updated 5/4/20
	'D1836': [220, 440, 500, 850], # updated 5/4/2020
	'D1879': [230, 370, 230, 360]  #updated 5/4/2020 

	  }
# Refine the region and update center position
#                 x, y
cen = { 'D1542': [83, 76], #all updated 6/12/2020
	'D1638': [410, 140],
	'D1688': [276, 494],
	'D1783': [622, 380],
	'D1836': [696, 311],
	'D1879': [285, 294]
	  }
	
# scale in pixels, last updated 7/2020
scale_dict = {  'D1542': 16,
	        'D1638': 31,
		'D1688': 45,
		'D1783': 42,
		'D1836': 52,
		'D1879': 41
	  }

# for dot detection on the viewer light image
dot_im = '/user/e18514/Documents/viewer-image-analysis/tiff_files/dots/dot1.tiff'
# Enter here the threshold (minimum intensity of peaks) to detect dots on image
detection_threshold = 0.1 
# Currently the dot detection on the viewers can be run standalone
# but can also be detected before each analysis by setting the flag below as True
detect_dots = False




