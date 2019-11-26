import numpy as np
import pandas as pd

#given a profile 
def profStats(prof, prof_err, xx):
    
    #run MC sim to sample a distribution of mean and std
    print("Calculating profile statistics...")
    i = 0
    iter_num = 50000
    xmc_data = [0 for i in range(0,iter_num)]
    
    while(i<iter_num):
        xmc_data[i] = np.random.normal(prof, prof_err)
        i = i + 1

    #get mean and std of each of the sampled distributions
    xmc_mean = [0 for i in range(0,iter_num)]
    xmc_mean_err= [0 for i in range(0,iter_num)]
    xmc_std = [0 for i in range(0,iter_num)]
    xmc_std_err = [0 for i in range(0,iter_num)]


    for k in range(0, iter_num):
        xmc_mean[k], xmc_mean_err[k] = findMean(xx, xmc_data[k], prof_err)
        #xmc_std[k], xmc_std_err[k] = findSTD(xx, xmc_data[k], xmc_mean[k], prof_err, xmc_mean_err[k])

    xmc_mean = np.array(xmc_mean)
    xmc_std = np.array(xmc_std)

    #calculate the mean and the std (non-weighted) of the result
    avg_mean = np.mean(xmc_mean)
    std_mean = np.std(xmc_mean)

    avg_std = np.mean(xmc_std)
    std_std = np.std(xmc_std)
    print(avg_mean)
    #return the mean of the means, the error on the mean
    #and the mean of the stds and the error on that
    return avg_mean, std_mean, avg_std, std_std


def findMean(xx, prof, prof_err):
    avg_x = []
    norm = []
    avg_xerr = []
    norm_err = []
    prof_err = np.asarray(prof_err)

    #weighted sum to get weighted average
    avg_x = np.sum(np.multiply(xx,prof))
    #sum of counts
    norm = np.sum(prof)

    #error propagation
    sig = np.abs(prof_err)/np.abs(prof)
    avg_xerr = np.multiply(sig,avg_x)
    norm_err = np.sqrt(np.sum(prof_err**2))

    avg = avg_x/norm
    #avg_err = avg*np.sqrt((avg_xerr/avg_x)**2 + (norm_err/norm)**2)
    avg_err = avg*(np.abs(prof_err)/np.abs(prof))
    return avg, avg_err

def findSTD(xx, prof, avg, prof_err, avg_err):
    #prof = prof[int(avg-100):int(avg+100)]
    #xx = xx[int(avg-100):int(avg+100)]
    prof_err = np.asarray(prof_err)

    mean_diff = 0
    weighted_diff = 0
    norm = 0

    #in the x axis the summed weighted diff is coming out negative
    #and in the y axis the sum of the weights is as well acouple of times
    #this gives a nan when we take the sqrt
    #both these fixes don't make sense when plotted
    #mean also seems a little off in image 09 and possibly others

    mean_diff = (xx - avg)**2
    weighted_diff = np.abs(np.sum(prof*mean_diff))
    norm = np.abs(np.sum(prof))

    #error propagation
    weighted_err= np.multiply(np.sqrt((prof_err/prof)**2 + (avg_err/avg)**2), weighted_diff)
    norm_err = np.sqrt(np.sum(prof_err**2))
    
    std = np.sqrt(weighted_diff/(norm*(1-1/len(prof))))
    
    #if (len(xx)==230):
        #print(std, weighted_diff, norm*(1-1/len(prof)) )
    
    std_err = std*np.sqrt((norm_err/norm)**2 + (weighted_err/weighted_diff)**2)
    return std, std_err