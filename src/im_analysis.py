### Image Analysis ###
import datetime
import sys
import warnings

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from statsmodels.stats.weightstats import DescrStatsW

from dot_detection import *
from im_reduction import *
from stats_profile import *

warnings.filterwarnings("ignore")

#Reducing selected tune and extracting beam profiles
image=Image(raw_image)
image.subtract_bg(bg)
image.get_profile()

y = np.arange(image.y_size)
x = np.arange(image.x_size)

#it's called x_smooth because that's what I called it in V1.0 or so when I was smoothing it
x_smooth = image.profile_x[200:330]
x_err = image.error_x[200:330]
x = x[200:330]
#clipping the y axis to get rid of noise for now
y_smooth = image.profile_y[:230]
y_err = image.error_y[:230]

y = y[:230]

#Find the mean and sigma of the data
#should all be in pixels
#print(repr(x_smooth), repr(y_smooth))

x_mean, x_mean_err, x_std, x_std_err = profStats(x_smooth, x_err, x)
y_mean, y_mean_err, y_std, y_std_err = profStats(y_smooth, y_err, y)

#print("x_mean, x_mean_err, x_std, x_std_err ", x_mean, x_mean_err, x_std, x_std_err)
#print("y_mean, y_mean_err, y_std, y_std_err ", y_mean, y_mean_err, y_std, y_std_err)

x_loc, y_loc= (x_mean-d1542_center[0]), (d1542_center[1]-y_mean) #y-axis is inverted
beam_loc=[x_mean, y_mean, x_std, y_std, x_loc*px_to_mm, y_loc*px_to_mm]


'''
f= open(f"data_arrays.txt", "a+")
f.write(f'{sys.argv[1][82:-5]} {np.transpose(x_smooth)}, {np.transpose(x)}, {np.transpose(y_smooth)}, {np.transpose(y)}')
f.close()
'''
#### plot and save results ####
mpl.style.use('seaborn')
fig = plt.figure(figsize=(16, 8))
grid = plt.GridSpec(16, 8, hspace=0, wspace=0)
main_ax = fig.add_subplot(grid[:-1, 1:]) 
#main_ax.get_xaxis().set_visible(False)
plt.setp(main_ax.get_xticklabels(), fontsize=0)
plt.setp(main_ax.get_yticklabels(), fontsize=0)

#Adding subplots for the profiles
y_hist = fig.add_subplot(grid[:-1, 1], sharey=main_ax)
x_hist = fig.add_subplot(grid[-1, 1:], sharex=main_ax)


#Plot the reduced image in center 
im=main_ax.imshow(image.subtracted_data,  cmap='cividis')
#cax = fig.add_axes([04.27, 0.8, 4.5, 0.05])
#fig.colorbar(im, cax=cax, orientation='vertical')
main_ax.grid(False)

try:
	main_ax.set_title(
		"Image: "+sys.argv[1][82:-5]+
		"\nCenter X-pos: %.1f +/- %.1f mm, Center Y-pos: %.1f +/- %.1f mm" 
		%(beam_loc[4], x_std*px_to_mm, beam_loc[5], y_std*px_to_mm),
		fontsize=11
		)
except NameError:
	main_ax.set_title(
		"Image: "+sys.argv[1][82:-5]+
		"\nScale: Not found\nRaw Center X-pos: %.1f +/- %.1f px, Center Y-pos: %.1f +/- %.1f px"
		%(x_mean, x_std, y_mean, y_std),
		fontsize=11
		)

main_ax.plot([0, image.shape[1]], [y_mean,y_mean],
            linewidth=0.6, color='r'
			)
main_ax.plot( [x_mean, x_mean], [0, image.shape[0]],
            linewidth=0.6, color='r'
			)

#Plotting dots. Their location is relative to to selected region of the light_image
main_ax.plot(d1542_dots[0][:], d1542_dots[1][:],
            'o', markeredgecolor='red', markerfacecolor='red', markersize=3
			)

# plot the x and y profiles
#orange=(200/255,82/255,0/255)
x_hist.plot(x, x_smooth)
x_hist.plot([x_mean,x_mean],[0, np.max(x_smooth)],
            linewidth=0.6, color='r', marker='.', markersize=4, label="Mean"
			)
x_hist.plot([x_mean+x_std,x_mean+x_std],[0, np.max(x_smooth)],
            linewidth=0.45, color='b', marker='.', markersize=4, label=u"\u00B11\u03C3"
			)
x_hist.plot([x_mean-x_std,x_mean-x_std],[0, np.max(x_smooth)],
            linewidth=0.45, color='b', marker='.', markersize=4
			)
x_hist.legend(loc="upper right", prop={'size':9})
#xticks=[i for i in range(x.max()) if i%20==0]
#x_hist.set_xticks(xticks)
plt.xticks(rotation=30)

y_hist.plot(y_smooth, y)
y_hist.plot([0, np.max(y_smooth)], [y_mean, y_mean], 
            linewidth=0.6, color='r', marker='.', markersize=4, label="Mean"
			)
y_hist.plot([0, np.max(y_smooth)], [y_mean+y_std, y_mean+y_std], 
            linewidth=0.45, color='b', marker='.', markersize=4, label=u"\u00B11\u03C3"
			)
y_hist.plot([0, np.max(y_smooth)], [y_mean-y_std, y_mean-y_std], 
            linewidth=0.45, color='b', marker='.', markersize=4
			)
#yticks= [i for i in range(y.max()) if i%20==0]
#y_hist.set_yticks(yticks)
y_hist.invert_xaxis()


#check that paths exists/create it
mkdir_p(output_path)
#save results
'''
f= open(f"data_mean_stdev_fullarray_{bin_f}pix.txt", "a+")
f.write(f'{sys.argv[1][82:-5]} {x_mean} {x_std} {y_mean} {y_std} {x_mean*px_to_mm} {x_std*px_to_mm} {y_mean*px_to_mm} {y_std*px_to_mm}\n')
f.close()
'''

timestring = (datetime.datetime.now()).strftime("%m-%d_%H:%M.%f")
image_name= viewer_loc + '_' + timestring
plt.savefig(output_path + 'ViewerCenter' + image_name + '.png', dpi=300)

'''
np.savetxt(output_path + 'BeamLoc_' + image_name + '.csv',
          [beam_loc], 
          header="X-Mean (px), Y-Mean (px), X-Peak (px), Y-Peak (px), X-Location (mm), Y-Location (mm)"
 )'''

f= open(f"{output_path}/data_mean_stdev_pix.txt", "a+")
f.write(f'{sys.argv[1][82:-5]} {x_mean} {x_mean_err} {x_std} {x_std_err} {y_mean} {y_mean_err} {y_std} {y_std_err}\n')
f.close()

np.savetxt(output_path + 'Xarray_' + image_name + '.csv', np.transpose([x_smooth, x]))
np.savetxt(output_path + 'Yarray_' + image_name + '.csv', np.transpose([y_smooth, y]))

if (show_plots== True):
	plt.show()
