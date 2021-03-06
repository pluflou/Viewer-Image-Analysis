### Image Analysis ###
import datetime
import sys
import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
#import scipy.signal as signal
#from lmfit import Model
#from lmfit.models import GaussianModel, SkewedGaussianModel, LorentzianModel, VoigtModel
from scipy.signal import savgol_filter

from dot_detection import *
from im_reduction import *

warnings.filterwarnings("ignore")

#Reducing selected tune and extracting beam profiles
image=Image(raw_image)
image.subtract_bg(bg)
image.get_profile()

#Apply a smoothing Savitzky-Golay filter to the arrays: applies a polynomial of order 3 for every 5 data points
y_smooth=savgol_filter(image.profile_y, 5, 3)
x_smooth=savgol_filter(image.profile_x, 5, 3)

#Fit the profiles to selected models and find the point where the median of the data lays
#x_med, x_sigp, x_sign =models[x_profile_model](x_smooth,x)
#y_med, y_sigp, y_sign =models[y_profile_model](y_smooth,y)

#UPDATE 2/12/19:
#instead of fitting with a model, take the median. Comparing to actual peak can give an idea of error.
x_med, x_sigp, x_sign = findMedian(x_smooth)
y_med, y_sigp, y_sign = findMedian(y_smooth)

x_peak, x_peak_idx= x_smooth.max(), list(x_smooth).index(x_smooth.max())
y_peak, y_peak_idx= y_smooth.max(), list(y_smooth).index(y_smooth.max())

x_loc, y_loc= (x_med-d1542_center[0]), (d1542_center[1]-y_med) #y-axis is inverted
beam_location=[x_med, y_med, x_peak_idx, y_peak_idx, x_loc*px_to_mm, y_loc*px_to_mm]

#### plot and save results ####
y = np.arange(image.y_size)
x = np.arange(image.x_size)

mpl.style.use('seaborn')
fig = plt.figure(figsize=(7, 5))
grid = plt.GridSpec(5, 7, hspace=0, wspace=0)
main_ax = fig.add_subplot(grid[:-1, 1:])

#main_ax.get_xaxis().set_visible(False)
plt.setp(main_ax.get_xticklabels(), fontsize=0)
plt.setp(main_ax.get_yticklabels(), fontsize=0)

#Adding subplots for the profiles
y_hist = fig.add_subplot(grid[:-1, 1], sharey=main_ax)
x_hist = fig.add_subplot(grid[-1, 2:6], sharex=main_ax)

#Plot the reduced image in center 
im=main_ax.imshow(image.subtracted_data,  cmap='cividis')
#cax = fig.add_axes([04.27, 0.8, 4.5, 0.05])
#fig.colorbar(im, cax=cax, orientation='vertical')
main_ax.grid(False)

try:
	main_ax.set_title(
		"Image: " + sys.argv[1] + 
		"\nScale: %.1f mm is 1 pixel\nCenter X-pos: %.1f +/- %.1f mm, Center Y-pos: %.1f +/- %.1f mm" 
		%(px_to_mm, beam_location[4], abs(x_peak_idx-x_med)*px_to_mm, beam_location[5], abs(y_peak_idx-y_med)*px_to_mm),
		fontsize=11
		)
except NameError:
	main_ax.set_title(
		"Image: "+sys.argv[1]+
		"\nScale: Not found\nRaw Center X-pos: %.1f +/- %.1f px, Center Y-pos: %.1f +/- %.1f px"
		%(abs(x_med), abs(x_peak_idx-x_med), abs(y_med), abs(y_peak_idx-y_med)), 
		fontsize=11
		)
	
main_ax.plot([0, image.shape[1]], [y_med,y_med],
            linewidth=0.6, color='r'
			)
main_ax.plot( [x_med, x_med], [0, image.shape[0]],
            linewidth=0.6, color='r'
			)

#Plotting dots. Their location is relative to to selected region of the light_image
#main_ax.plot(d1542_dots[0][:], d1542_dots[1][:],
 #           'o', markeredgecolor='red', markerfacecolor='red', markersize=3
#			)

# plot the x and y profiles
#orange=(200/255,82/255,0/255)
x_hist.plot(x, image.profile_x)
x_hist.plot([x_med,x_med],[0, x_peak],
            linewidth=0.6, color='r', marker='.', markersize=4, label="Median"
			)
x_hist.plot([x_peak_idx,x_peak_idx],[0, x_peak],
            linewidth=0.6, color='gray', linestyle='-', label="Peak"
			)
x_hist.legend(loc="upper right", prop={'size':8})
xticks=[i for i in range(image.x_size) if i%20==0]
x_hist.set_xticks(xticks)
plt.xticks(rotation=30)

y_hist.plot(image.profile_y, y)
y_hist.plot([0, y_peak], [y_med, y_med], 
            linewidth=0.6, color='r', marker='.', markersize=4, label="Median"
			)
y_hist.plot([0, y_peak], [y_peak_idx, y_peak_idx],
            linewidth=0.6, color='gray',  linestyle='-', label="Peak"
			)
yticks= [i for i in range(image.y_size) if i%20==0]
y_hist.set_yticks(yticks)
y_hist.invert_xaxis()

#check that paths exists/create it
mkdir_p(output_path)

#save results
timestring = (datetime.datetime.now()).strftime("%m-%d_%H:%M.%f")
image_name= viewer_loc + '_' + timestring
#plt.savefig(output_path + 'ViewerCenter' + image_name + '.png', dpi=300)
#np.savetxt(output_path + 'BeamLoc_' + image_name + '.csv',
#          [beam_location], 
#          header="X-Median (px), Y-Median (px), X-Peak (px), Y-Peak (px), X-Location (mm), Y-Location (mm)"
# )

if (show_plots== True):
	plt.show()
