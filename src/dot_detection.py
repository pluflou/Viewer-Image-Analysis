### Viewer Dots Detection ###
from INPUT import *
import numpy as np
import matplotlib.pyplot as plt
import math
from skimage.feature import match_template, peak_local_max
import warnings
warnings.filterwarnings("ignore")

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
        #print("Dots detected in ROI are at:\n", peaks)
        dots_in_image= [x_min+peaks[:,1],peaks[:,0]+y_min]
        print("Dots in original image are at [X,Y]: \n", dots_in_image)
        flag= False
        continue
    else:
        print("Couldn't find threshold.")

#Getting the distance between dots
dx=[] #distances between each dots with equal x-position
dy=[]

for j in range(len(peaks)-1):
    for i in range(len(peaks)): #loop over all points
       # print(j, i, peaks[j][0], peaks[i][0])
        if ((peaks[j][0]==peaks[i][0])& (j!=i)):  #find dots that share x-position
            dist = math.hypot(peaks[j][0]-peaks[i][0], peaks[j][1]-peaks[i][1])
            dx.append(dist)
            #print(j, i, peaks[j][0], peaks[i][0], dist, dx)

       # print(j, i, peaks[j][0], peaks[i][0])
        if ((peaks[j][1]==peaks[i][1])& (j!=i)): #find dots that share y-position
            dist = math.hypot(peaks[j][0]-peaks[i][0], peaks[j][1]-peaks[i][1])
            dy.append(dist)
            #print(j, i, peaks[j][1], peaks[i][1], dist, dy)

#select the correct distance corresponding to two dots separated by 5mm
try:
    scale_x=min(dx)
    print("5 mm (x-dir) correspond to ", scale_x, " pixels.")
except ValueError:
    print("Could not find dots on same x-axis")
try:
    scale_y=min(dy)
    print("5 mm (y-dir) correspond to ", scale_y, " pixels.")
except ValueError:
    print("Could not find dots on same y-axis")

if (len(dy)!=0 and len(dx)!=0):
    if (scale_x<= scale_y):
        scale= scale_x
        print("Adopted scale is ",scale," pixels for 5 mm.")
    elif (scale_y<= scale_x):
        scale= scale_y
        print("Adopted scale is ",scale," pixels for 5 mm.")
elif (len(dy)!=0 and len(dx)==0):
    scale= scale_y
elif (len(dx)!=0 and len(dy)==0):
    scale= scale_x
else:
    scale = 1
    print("No scale was found.")

#setting conversion
px_to_mm= 5/scale

d1542_center= [83, 83] #x,y -- update this when viewer moves in the screen

#recreating the correct dots on viewer to plot
d1542_dots=[[d1542_center[0],d1542_center[0],d1542_center[0], d1542_center[0]+ scale, 
            d1542_center[0]- scale],
[d1542_center[1]+scale,d1542_center[1]-scale,d1542_center[1],d1542_center[1],d1542_center[1]]]
	    
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
# x locations are second column of peaks array. (x is columns and y is rows of raw image)
ax3.autoscale(False)
ax3.plot(peaks[:,1], peaks[:,0], 'o', markeredgecolor='r', markerfacecolor='none', markersize=10)
for row in peaks:
    ax3.text(row[1],row[0],(x_min+row[1],y_min+row[0]))
#plt.show()








