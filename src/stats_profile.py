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
        xmc_mean[k] = findMean(xx, xmc_data[k])
        xmc_std[k] = findSTD(xx, xmc_data[k], xmc_mean[k])
    
    #added this variable to pass array to save the data for plotting
    pr_mean= (xmc_mean)
    
    xmc_mean = np.array(xmc_mean)
    xmc_std = np.array(xmc_std)

    #calculate the mean and the std (non-weighted) of the result
    avg_mean = np.mean(xmc_mean)
    std_mean = np.std(xmc_mean)

    avg_std = np.mean(xmc_std)
    std_std = np.std(xmc_std)

    #return the mean of the means, the error on the mean
    #and the mean of the stds and the error on that
    
    return avg_mean, std_mean, avg_std, std_std, pr_mean


def findMean(xx, prof):
    avg_x = []
    norm = []

    #weighted sum to get weighted average
    avg_x = np.sum(np.multiply(xx,prof))
    #sum of counts
    norm = np.sum(prof)

    avg = avg_x/norm
    return avg

def findSTD(xx, prof, avg):
    #prof = prof[int(avg-100):int(avg+100)]
    #xx = xx[int(avg-100):int(avg+100)]

    mean_diff = 0
    weighted_diff = 0
    norm = 0

    mean_diff = (xx - avg)**2
    weighted_diff = np.abs(np.sum(prof*mean_diff))
    norm = np.abs(np.sum(prof))
    
    std = np.sqrt(weighted_diff/(norm*(1-1/len(prof))))
    return std