### Image Analysis ###
from INPUT import *
from dot_detection import *
from im_reduction import *
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
x_mid=models[x_profile_model](x_smooth,x)
y_mid=models[y_profile_model](y_smooth,y)


#### plot and save results ####
fig = plt.figure(figsize=(6, 4))
grid = plt.GridSpec(5, 5, hspace=0.3, wspace=0)
main_ax = fig.add_subplot(grid[:-1, 1:])
plt.text(260, 5, "Data Midpoint: X=%.1f, Y=%.1f, Scale: 5 mm is %.1f pixels" %(x_mid, y_mid, scale), size=9,
         ha="right", va="top",
         bbox=dict(boxstyle="round",
                   ec=(0, 0, 0.5),
                   fc=(1, 1, 1),
                   )
         )
#Adding subplots for the profiles
y_hist = fig.add_subplot(grid[:-1, 0], sharey=main_ax)
x_hist = fig.add_subplot(grid[-1, 1:], sharex=main_ax)

#Plot the reduced image in center 
main_ax.imshow(image.subtracted_data)
main_ax.plot([0, image.shape[1]], [y_mid,y_mid], linewidth=1, color='r')
main_ax.plot( [x_mid, x_mid], [0, image.shape[0]], linewidth=1, color='r')
#Plotting dots. Their location is relative to to selected region of the light_image
main_ax.plot(x_min+peaks[:,1], peaks[:,0]+y_min,  'o', markeredgecolor='r', markerfacecolor='none', markersize=5)

# plot the x and y profiles
x_hist.plot(x, image.profile_x)
x_hist.plot([x_mid,x_mid],[0, image.profile_x.max()],  linewidth=0.6, color='r', marker='.')

y_hist.plot(image.profile_y, y)
y_hist.plot([0, image.profile_y.max()], [y_mid, y_mid], linewidth=0.6, color='r', marker='.')
#y_hist.invert_yaxis()
y_hist.invert_xaxis()

plt.show()
#plt.savefig('results.png', dpi=100)




