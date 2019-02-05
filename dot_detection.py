### Viewer Dots Detection ###
from INPUT import *
import numpy as np
import matplotlib.pyplot as plt
import math
from skimage.feature import match_template, peak_local_max



#Define the center region that surrounds the 5 center dots

light_image_region=light_image[y_min:y_max,x_min:x_max]

#Find matched of the dot template selected
result = match_template(light_image_region, template, pad_input=True) 

flag = True
while (flag):
    peaks = peak_local_max(result,min_distance=2,threshold_rel=threshold) # find our peaks
    if (peaks.shape[0]>5):
        threshold +=0.05
        #print(peaks.shape)
    elif (peaks.shape[0]<=5):
        print("Dots detected are at:\n", peaks)
        flag= False
        continue
    else:
        print("Couldn't find threshold.")

#Show the image, template and dots detected        
fig = plt.figure(figsize=(5, 5))
ax1 = plt.subplot(1, 3, 1)
ax2 = plt.subplot(1, 3, 2)
ax3 = plt.subplot(1, 3, 3, sharex=ax2, sharey=ax2)

ax1.imshow(template, cmap=plt.cm.gray)
ax1.set_axis_off()
ax1.set_title('Template')

ax2.imshow(light_image_region, cmap=plt.cm.gray)
ax2.set_axis_off()
ax2.set_title('Image')

ax3.imshow(result)
ax3.set_axis_off()
ax3.set_title('Matching Results')
# highlight matched region
ax3.autoscale(False)
#ax3.plot(x, y, 'o', markeredgecolor='r', markerfacecolor='none', markersize=10)
ax3.plot(  peaks[:,1], peaks[:,0], 'o', markeredgecolor='r', markerfacecolor='none', markersize=10)








