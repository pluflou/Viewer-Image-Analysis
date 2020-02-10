import sys
import warnings

import numpy as np
warnings.filterwarnings("ignore")

class Image:    
    def __init__(self, image):
        self.raw = image
        self.shape= image.shape
        self.x_size= image.shape[1]
        self.y_size= image.shape[0]
        self.subtracted_data= np.array([[0 for x in range(self.x_size)] for y in range(self.y_size)])
        self.profile_x= [0 in range (self.x_size)]
        self.profile_y= [0 in range (self.y_size)]
        self.error_x= [0 in range (self.x_size)]
        self.error_y= [0 in range (self.y_size)]
        self.offset_x= 0 
        self.offset_y= 0
      
    def subtract_bg(self,bg):
        print("Subtracting background...")
        if (bg.shape == self.shape): 
            for i in range(self.y_size):
                for j in range (self.x_size):
                    #if ((self.raw[i][j]>bg[i][j]).all() and (bg[i][j]>=0).all() and (self.raw[i][j]>=0).all()):
                    self.subtracted_data[i][j]= int(self.raw[i][j])-int(bg[i][j])
                    self.error[i][j] = np.sqrt(np.abs(int(self.raw[i][j])) + np.abs(int(bg[i][j])))
            return self.subtracted_data
        else:
            print("Error: Background image size does not match data size.")
    
     def get_profile(self):
        print("Getting y-axis profile...")
        #PROFILE IN Y
        for i in range(self.y_size): #loop over all y
            sum=0
            err=0
            for j in range(self.x_size): #loop over all x for each y: gives one number
                sum=sum + self.subtracted_data[i][j]
                err = err + (self.error[i][j])**2

            self.profile_y.append(sum)
            self.error_y.append(np.sqrt(err))

        self.offset_y= np.mean(self.profile_y[1:15])
        self.profile_y=self.profile_y[1:]#- self.offset_y  
        self.error_y = self.error_y[1:]
    
     
        #PROFILE IN X
        print("Getting x-axis profile...")
        for i in range(self.x_size): #loop over all x
            sum=0
            err=0 
            for j in range(self.y_size): #loop over all y for each x: gives one number
                sum=sum + self.subtracted_data[j][i]
                err = err + (self.error[j][i])**2
            self.profile_x.append(sum)
            self.error_x.append(np.sqrt(err))

        self.offset_x=np.mean(self.profile_x[1:15])
        self.profile_x=self.profile_x[1:]#-self.offset_x
        self.error_x= self.error_x[1:]offset_x

def findMedian(profile):
    sum_total=sum(profile)
    median=0
    sigp=0
    sign=0
    for i in range(len(profile)):
        sumInt=sum(profile[0:i])
        frac=sumInt/sum_total
        if (frac>0.15 and frac<0.17):
            sign=i
        elif (frac>0.48 and frac<0.52):
            median=i
        elif (frac>0.45 and frac<0.54):
            median=i
        elif (frac>0.41 and frac<0.58):
            median=i
        elif (frac>0.83 and frac<0.85):
            sigp=i
    if (median==0):
        print("Error when finding median. Check im_reduction ln 62.")
    return  median, sigp, sign
