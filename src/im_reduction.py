import sys
import numpy as np
from lmfit import Model
from lmfit.models import GaussianModel, SkewedGaussianModel, LorentzianModel, VoigtModel
import warnings
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
        self.offset_x= 0 
        self.offset_y= 0
      
    def subtract_bg(self,bg):
        print("Subtracting background...")
        if (bg.shape == self.shape): 
            for i in range(self.y_size):
                for j in range (self.x_size):
                    if ((self.raw[i][j]>bg[i][j]).all() and (bg[i][j]>=0).all() and (self.raw[i][j]>=0).all()):
                        self.subtracted_data[i][j]= self.raw[i][j]-bg[i][j]
                    elif (bg[i][j]<0):
                        self.subtracted_data[i][j]= 0
            return self.subtracted_data
        else:
            print("Error: Background image size does not match data size.")
    
    def get_profile(self):
        print("Getting y-axis profile...")
        #PROFILE IN Y
        for i in range(self.y_size): #loop over all y
            sum=0
            for j in range(self.x_size): #loop over all x for each y: gives one number
                sum=sum + self.subtracted_data[i][j]
            self.profile_y.append(sum)
        self.offset_y= np.mean(self.profile_y[1:15])
        self.profile_y=self.profile_y[1:]- self.offset_y      
     
        #PROFILE IN X
        print("Getting x-axis profile...")
        for i in range(self.x_size): #loop over all x
            sum=0
            for j in range(self.y_size): #loop over all y for each x: gives one number
                sum=sum + self.subtracted_data[j][i]
            self.profile_x.append(sum)
        self.offset_x=np.mean(self.profile_x[1:15])
        self.profile_x=self.profile_x[1:]-self.offset_x

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

def skewedgauss_fit(profile, x):
    gauss = SkewedGaussianModel()
    params = gauss.guess(profile, x=x)
    output = gauss.fit(profile, params, x=x)
    
    #to plot the fit uncomment the line below
    #fig, gridspec = output.plot(data_kws={'markersize': 1})
    
    #find the maximum of the gaussian peak
    peak=np.array(output.best_fit).max()
    peak_index=list(output.best_fit).index(peak)

    #find the center of the distribution
    center_param=np.array(output.params['center'])
    #fwhm=np.array(output.params['fwhm'])
    
    #find the mid point that separates two equal amounts of data
    median, sigp, sign = findMedian(np.array(output.best_fit))
    #this mid point will be the 'effective center' of our beam spot
    #because this will make it easier to compare to the BCM data and it distributes the beam equally over the center
    return median, sigp, sign

def gauss_fit(profile, x):
    gauss = GaussianModel()
    params = gauss.guess(profile, x=x) 
    output = gauss.fit(profile, params, x=x)

    #to plot the fit uncomment the line below
    #fig, gridspec = output.plot(data_kws={'markersize': 1})
    median, sigp, sign = findMedian(np.array(output.best_fit))
    return median, sigp, sign

def doublegauss_fit(profile, x):
    gauss1 = GaussianModel(prefix='g1_') 
    gauss2= GaussianModel(prefix='g2_')

    params_1 = gauss1.make_params(amplitude=250000,center=145, sigma=1)
    params_2 = gauss2.make_params(amplitude=100000, center=170, sigma=1)
    pars = params_1.update(params_2)

    mod= gauss1 + gauss2 
    output = mod.fit(profile, params_1, x=x)
    median, sigp, sign =findMedian(np.array(output.best_fit))

    #to plot the fit uncomment the line below
    #fig, gridspec = output.plot(data_kws={'markersize': 1})
    
    #to find the center of the fit instead of mid point of data uncomment the section below
    #g1_c, g2_c=[np.array(output.params['g1_center']), np.array(output.params['g2_center'])]
    #g1_a, g2_a= [output.params['g1_amplitude'], output.params['g2_amplitude']] 
    #if (g1_a>g2_a):
     #   print(g1_c)
      #  return g1_c
    #elif (g2_a>g1_a):
     #   print(g2_c)
      #  return g2_c
    #else:
     #   print("Fit is weird.")

    return median, sigp, sign


def doubleSgauss_fit(profile, x):
    gauss1 = GaussianModel(prefix='g1_') #SkewedGaussianModel(prefix='g1_')
    gauss2= SkewedGaussianModel(prefix='g2_')

    params_1 = gauss1.make_params(amplitude=300000,center=300, sigma=1)
    params_2 = gauss2.make_params(amplitude=100000, center=170, sigma=1)
    pars = params_1.update(params_2)
    
    mod= gauss1 + gauss2 
    output = mod.fit(profile, params_1, x=x)
    median, sigp, sign =findMedian(np.array(output.best_fit))

    #to plot the fit uncomment the line below
    #fig, gridspec = output.plot(data_kws={'markersize': 1})

    #to find the center of the fit instead of mid point of data uncomment the section below
    #g1_c, g2_c=[np.array(output.params['g1_center']), np.array(output.params['g2_center'])]
    #g1_a, g2_a= [output.params['g1_amplitude'], output.params['g2_amplitude']]
    #if (g1_a>g2_a):
     #   return g1_c
    #elif (g2_a>g1_a):
     #   return g2_c
    #else:
      #  print("Fit is weird.")

    return median, sigp, sign

models= {'single_gaussian': gauss_fit , 'double_gaussian': doublegauss_fit , 'skewed_gaussian': skewedgauss_fit , 'gaussian_skewed_gaussian': doubleSgauss_fit }
