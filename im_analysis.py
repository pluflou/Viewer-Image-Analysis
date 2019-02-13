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
x_med, x_sigp, x_sign =models[x_profile_model](x_smooth,x)
y_med, y_sigp, y_sign =models[y_profile_model](y_smooth,y)
#UPDATE 2/12/19:
#instead of fitting with a model, take range that contains of 68% of data without fitting
#x_med, x_sigp, x_sign = findMedian(x_smooth)
#y_med, y_sigp, y_sign = findMedian(y_smooth)

#### plot and save results ####
fig = plt.figure(figsize=(10, 7))
grid = plt.GridSpec(5, 5, hspace=0.35, wspace=0)
main_ax = fig.add_subplot(grid[:-1, 1:])
#plt.text(210, 5, "Data Median: X=%.1f, Y=%.1f\n Viewer Center: \n Scale: 1 mm is %.1f pixels" %(x_med, y_med, scale/5), size=10,
#         ha="right", va="top",
#         bbox=dict(boxstyle="round",
#                   ec=(0, 0, 0.5),
#                   fc=(1, 1, 1),
#                   )
#        )
#Adding subplots for the profiles
y_hist = fig.add_subplot(grid[:-1, 0], sharey=main_ax)
x_hist = fig.add_subplot(grid[-1, 1:], sharex=main_ax)

#Plot the reduced image in center 
main_ax.imshow(image.subtracted_data)
main_ax.set_title("Image: "+sys.argv[1]+ "\nScale: %.1f pixels is 1 mm\nData Median: X=%.1f, Y=%.1f, Viewer Center: Enter manually" %(scale/33, x_med, y_med), fontsize=12)
main_ax.plot([0, image.shape[1]], [y_med,y_med], linewidth=1, color='r')
main_ax.plot( [x_med, x_med], [0, image.shape[0]], linewidth=1, color='r')
#Plotting dots. Their location is relative to to selected region of the light_image
main_ax.plot(x_min+peaks[:,1], peaks[:,0]+y_min,  'o', markeredgecolor='r', markerfacecolor='none', markersize=5)
print("Dots are at: \n X:", x_min+peaks[:,1]," Y: ", peaks[:,0]+y_min)
# plot the x and y profiles
x_hist.plot(x, image.profile_x)
x_hist.plot([x_med,x_med],[0, image.profile_x.max()],  linewidth=0.6, color='r', marker='.')
x_hist.plot([x_sigp,x_sigp],[0, image.profile_x.max()],  linewidth=0.6, color='r', linestyle='-')
x_hist.plot([x_sign,x_sign],[0, image.profile_x.max()],  linewidth=0.6, color='r',  linestyle='-')
x_hist.set_xlabel("Center Range between %.1f and %.1f pixels" %(x_sign, x_sigp), fontsize=11)

y_hist.plot(image.profile_y, y)
y_hist.plot([0, image.profile_y.max()], [y_med, y_med], linewidth=0.6, color='r', marker='.')
y_hist.plot([0, image.profile_y.max()], [y_sign, y_sign], linewidth=0.6, color='r',  linestyle='-')
y_hist.plot([0, image.profile_y.max()], [y_sigp, y_sigp], linewidth=0.6, color='r',  linestyle='-')
y_hist.set_title("Center Range between\n%.1f and %.1f pixels" %(y_sign, y_sigp), fontsize=11)
#y_hist.invert_yaxis()
y_hist.invert_xaxis()

#t= pd.to_datetime
timestring = (datetime.datetime.now()).strftime("%m-%d_%H:%M")
plt.savefig('ViewerCenter'+'_'+timestring+'.png', dpi=300)
plt.show()
 




