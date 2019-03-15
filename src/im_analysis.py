### Image Analysis ###
from INPUT import *
from dot_detection import *
from im_reduction import *
import datetime
import sys
import numpy as np
import matplotlib.pyplot as plt 
import scipy.signal as signal
from lmfit import Model
from lmfit.models import GaussianModel, SkewedGaussianModel, LorentzianModel, VoigtModel
from scipy.signal import savgol_filter
import warnings
warnings.filterwarnings("ignore")

#Reducing selected tune and extracting beam profiles
image=Image(raw_image)
image.subtract_bg(bg)
image.get_profile()
y = np.arange(image.y_size)
x = np.arange(image.x_size)

#Apply a smoothing Savitzky-Golay filter to the arrays: applies a polynomial of order 3 for every 5 data points
y_smooth=savgol_filter(image.profile_y, 5, 3)
x_smooth=savgol_filter(image.profile_x, 5, 3)

#Fit the profiles to selected models and find the point where the median of the data lays
#x_med, x_sigp, x_sign =models[x_profile_model](x_smooth,x)
#y_med, y_sigp, y_sign =models[y_profile_model](y_smooth,y)
#UPDATE 2/12/19:
#instead of fitting with a model, take range that contains of 68% of data without fitting
x_med, x_sigp, x_sign = findMedian(x_smooth)
y_med, y_sigp, y_sign = findMedian(y_smooth)
x_peak, x_peak_idx= x_smooth.max(), list(x_smooth).index(x_smooth.max())
y_peak, y_peak_idx= y_smooth.max(), list(y_smooth).index(y_smooth.max())

#### plot and save results ####
fig = plt.figure(figsize=(9, 5))
grid = plt.GridSpec(5, 7, hspace=0.35, wspace=0)
main_ax = fig.add_subplot(grid[:-1, 1:])
plt.setp(main_ax.get_xticklabels(), fontsize=6)
plt.setp(main_ax.get_yticklabels(), fontsize=6)
#Adding subplots for the profiles
y_hist = fig.add_subplot(grid[:-1, 1], sharey=main_ax)
x_hist = fig.add_subplot(grid[-1, 2:6], sharex=main_ax)

#Plot the reduced image in center 
main_ax.imshow(image.subtracted_data)
try:
	main_ax.set_title("Image: "+sys.argv[1]+ "\nScale: %.1f mm is 1 pixel\nCenter X-pos: %.1f +/- %.1f mm, Center Y-pos: %.1f +/- %.1f mm" %(5/scale, abs(x_med-84)*(5/scale), abs(x_peak_idx-x_med)*(5/scale), abs(y_med-82)*(5/scale), abs(y_peak_idx-y_med)*(5/scale)), fontsize=12)
#Data Median: X=%.1f, Y=%.1f, Viewer Center: X=169, Y=164#
except NameError:
	main_ax.set_title("Image: "+sys.argv[1]+ "\nScale: Not found\nRaw Center X-pos: %.1f +/- %.1f px, Center Y-pos: %.1f +/- %.1f px" %(abs(x_med), abs(x_peak_idx-x_med), abs(y_med), abs(y_peak_idx-y_med)), fontsize=12)
	
main_ax.plot([0, image.shape[1]], [y_med,y_med], linewidth=1, color='r')
main_ax.plot( [x_med, x_med], [0, image.shape[0]], linewidth=1, color='r')
#Plotting dots. Their location is relative to to selected region of the light_image
main_ax.plot(x_min+peaks[-2,1], peaks[-2,0]+y_min,  'o', markeredgecolor='r', markerfacecolor='none', markersize=5)

print("Dots are at: \n X:", x_min+peaks[:,1]," Y: ", peaks[:,0]+y_min)

# plot the x and y profiles
orange=(200/255,82/255,0/255)
x_hist.plot(x, image.profile_x)
x_hist.plot([x_med,x_med],[0, x_peak],  linewidth=0.6, color='r', marker='.', markersize=4, label="Median")
x_hist.plot([x_peak_idx,x_peak_idx],[0, x_peak],  linewidth=0.6, color=orange, linestyle='-', label="Peak")
x_hist.legend(loc="upper right", prop={'size':8})


y_hist.plot(image.profile_y, y)
y_hist.plot([0, y_peak], [y_med, y_med], linewidth=0.6, color='r', marker='.', markersize=4, label="Median")
y_hist.plot([0, y_peak], [y_peak_idx, y_peak_idx], linewidth=0.6, color=orange,  linestyle='-', label="Peak")
y_hist.invert_xaxis()


timestring = (datetime.datetime.now()).strftime("%m-%d_%H:%M.%f")
plt.savefig('output/ViewerCenter'+'_'+timestring+'.png', dpi=300)
plt.show()
 




