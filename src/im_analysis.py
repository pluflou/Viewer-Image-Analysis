### Image Analysis ###
import datetime
import sys
import warnings

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import stats
from statsmodels.stats.weightstats import DescrStatsW

from INPUT import *
from dot_detection import *
from im_reduction import *
from stats_profile import *

warnings.filterwarnings("ignore")

show_plots = True

#Reducing selected tune and extracting beam profiles
image =Image(raw_image)
image.subtract_bg(bg)

#smoothing 
#image = imageraw.smooth

image.get_profile()
y = np.arange(image.y_size)
x = np.arange(image.x_size)

#it's called x_smooth because that's what I called it in V1.0 or so when I was smoothing it
x_smooth = image.profile_x#[200:330]
x_err = image.error_x#[200:330]
x_ax = x#[200:330]

#clipping the y axis to get rid of noise for now
y_smooth = image.profile_y#[:220]
y_err = image.error_y#[:220]
y_ax = y#[:220]

######### uncomment this section to calculate the weighted mean using a MC process #########################
'''
#Find the mean and sigma of the data
#should all be in pixels
x_mean, x_mean_err, x_std, x_std_err, mean_arr_x = profStats(x_smooth, x_err, x_ax)
y_mean, y_mean_err, y_std, y_std_err, mean_arr_y = profStats(y_smooth, y_err, y_ax)


x_loc, y_loc= (x_mean-viewer_center[0]), (viewer_center[1]-y_mean) #y-axis is inverted
beam_loc=[x_mean, y_mean, x_std, y_std, x_loc*px_to_mm, y_loc*px_to_mm, x_mean_err, y_mean_err]

#uncomment this to save MC simulation data for mean distribution plotting
#np.savetxt('im32_data_array_x.txt', mean_arr_x, delimiter=' ') 

#'''
#############################################################################################################
#############################################################################################################
#############################################################################################################
######### if you want to use the median instead of the weighted mean, uncomment the section below ###########
#'''

#the mean is actually a median in this case
x_mean, x_nsig, x_psig = findMedian(x_smooth)
y_mean, y_nsig, y_psig = findMedian(y_smooth) #do not actually need the width in y 

#print("Test digits {0:.4f} {1:.4f}".format(x_mean, y_mean))

x_peak, x_idx= np.max(x_smooth), list(x_smooth).index(np.max(x_smooth)) 
y_peak, y_idx= np.max(y_smooth), list(y_smooth).index(np.max(y_smooth))


x_loc, y_loc= (x_mean-viewer_center[0]), (viewer_center[1]-y_mean) #y-axis is inverted

#print("Center location", viewer_center[0], viewer_center[1], "xsize", image.x_size, "ysize", image.y_size)

#taking x and y in pixels, indices 0 and 1
beam_loc=[x_mean, y_mean, x_idx, y_idx, x_loc, y_loc, x_peak, y_peak, x_nsig, x_psig]

#'''
#############################################################################################################

#fig1= plt.figure(figsize=(7,5))
#plt.imshow(raw_image)

#### plot and save results ####
mpl.style.use('seaborn')
fig = plt.figure(figsize=(7, 5))
grid = plt.GridSpec(5, 7, hspace=0, wspace=0)
main_ax = fig.add_subplot(grid[:-1, 1:])

#main_ax.get_xaxis().set_visible(False)
plt.setp(main_ax.get_xticklabels(), fontsize=10)
plt.setp(main_ax.get_yticklabels(), fontsize=10)

#Adding subplots for the profiles
y_hist = fig.add_subplot(grid[:-1, 1], sharey=main_ax)
x_hist = fig.add_subplot(grid[-1, 2:6], sharex=main_ax)

#Plot the reduced image in center 
im=main_ax.imshow(image.subtracted_data,  cmap='cividis')

main_ax.grid(False)

#try:
#main_ax.set_title("Image: " +sys.argv[1].split('captures/')[1]+ "\nScale: %.1f mm is 1 pixel\nCenter X-pos: %.1f +/- %.1f mm, Center Y-pos: %.1f +/- %.1f mm" %(px_to_mm, beam_loc[4], abs(x_idx-x_mean)*px_to_mm, beam_loc[5], abs(y_idx-y_mean)*px_to_mm), fontsize=11)
#except NameError:

main_ax.set_title("Image: " +sys.argv[1].split('2020/')[1]+ "\nRaw Center X-pos: %.1f +/- %.1f px, Center Y-pos: %.1f +/- %.1f px \n With X-dir: %.1f px" %(x_mean, abs(x_idx-x_mean), y_mean, abs(y_idx-y_mean), x_psig-x_nsig), fontsize=11)
	
main_ax.plot([0, image.shape[1]], [y_mean,y_mean], linewidth=0.6, color='r')
main_ax.plot( [x_mean, x_mean], [0, image.shape[0]], linewidth=0.6, color='r')

#Plotting dots. Their location is relative to to selected region of the light_image
main_ax.plot(viewer_dots[0][:], viewer_dots[1][:],  'o', markeredgecolor='red', markerfacecolor='red', markersize=3)

# plot the x and y profiles
x_hist.plot(x_ax, x_smooth)
x_hist.plot([x_mean,x_mean],[0, np.max(x_smooth)],
            linewidth=0.6, color='r', marker='.', markersize=4, label="Mean"
			)
x_hist.plot( [0, len(image.profile_x)],[0, 0],
            linewidth=0.6, color='gray', marker='.', markersize=0
			)
x_hist.plot( [x_nsig, x_nsig], [0, np.max(x_smooth)],
            linewidth=0.45, color='b', marker='.', markersize=4, label=u"\u00B11\u03C3"
			)
x_hist.plot( [x_psig, x_psig], [0, np.max(x_smooth)],
           linewidth=0.45, color='b', marker='.', markersize=4
			)
x_hist.legend(loc="upper right", prop={'size':8})
xticks=[i for i in range(image.x_size) if i%20==0]
x_hist.set_xticks(xticks)
plt.xticks(rotation=45)

y_hist.plot(y_smooth, y_ax)
y_hist.plot([0, np.max(y_smooth)], [y_mean, y_mean], 
            linewidth=0.6, color='r', marker='.', markersize=4, label="Mean"
			)
y_hist.plot([0, 0], [0, len(image.profile_y)], 
            linewidth=0.6, color='gray', marker='.', markersize=0
			)

#y_hist.plot([0, np.max(y_smooth)], [y_mean+y_mean_err, y_mean+y_mean_err], 
 #           linewidth=0.45, color='b', marker='.', markersize=4, label=u"\u00B11\u03C3"
	#		)
#y_hist.plot([0, np.max(y_smooth)], [y_mean-y_mean_err, y_mean-y_mean_err], 
 #          linewidth=0.45, color='b', marker='.', markersize=4
	#		)
yticks= [i for i in range(image.y_size) if i%20==0]
y_hist.set_yticks(yticks)
y_hist.invert_xaxis()

#check that paths exists/create it
mkdir_p(output_path)

#save results

#uncommment this to save the different stats for a single run
#f= open(  output_path + f"data_output_stats_report.txt", "a+")
#f.write(f'{sys.argv[1][90:-5]} {x_mean} {x_mean_err} {x_std} {y_mean} {y_mean_err} {y_std} {x_mean*px_to_mm} {x_std*px_to_mm} {y_mean*px_to_mm} {y_std*px_to_mm}\n')
#f.close()

image_name= sys.argv[1].split("2020/")[1].split(".tiff")[0] #+ timestring

#this is the text file the optimizer looks for to calculate the distance
np.savetxt(output_path + 'BeamLoc_' + image_name + '.csv',
          [beam_loc] )
          #header="X-Mean (px), Y-Mean (px), X-Peak (px), Y-Peak (px), X-Location (mm), Y-Location (mm), errorx/nsig (px), errory/psig (px)"


#timestring = (datetime.datetime.now()).strftime("%m-%d_%H:%M.%f")
#plt.savefig(f'/user/e18514/Documents/viewer-image-analysis/output/optimizer/{image_name}.png', dpi=300)


#np.savetxt('/user/e18514/Documents/Viewer-Image-Analysis/output/optimizer/BeamLoc_' + image_name + '.csv', [beam_location])
#header="X-Median (px), Y-Median (px), X-Peak (px), Y-Peak (px), X-Location (mm), Y-Location (mm), x_mean_err (px), y_mean_err (px)"


if (show_plots == True):
	plt.show()

