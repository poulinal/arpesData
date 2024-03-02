import numpy as np
from PIL import Image
from get_dataV2 import get_tiff, tiff_names


def getSum(df, resources):# Calculate and return the sum of all Tiff files in the form of an array
    sumTiff = 0
    allTif = tiff_names(df)
    #print(allTif)
    #xLim = 0 #for dev utils
    tifIm = []

    for tiffName in allTif: #note this version is for development, the for below is correct for use
    #for tiffName in allTif: #iterate through all tiff files (tiffName is the uARPES_restest_***)
        #print(tiffName)
        tiffFile = Image.open(resources + '\\' + tiffName) #open the tiff file
        imArray = np.array(tiffFile) #put the image into an array
        tifIm.append(imArray) #saves the tiff image array
        sumTiff += imArray #add tiff pixel values to the sum array
        
        # for dev utils
        #xLim += 1
        #if xLim==3:
        #    break
        # for dev utils ^
        
    return sumTiff #return the average

def getAvg(df, sumTiff): # return the average tiff values in the form of an arrray
    averageTIFF = sumTiff / int(get_tiff(df)) # divide each element of the sum array by the number of tiff files
    return averageTIFF


def tiffIm(df, resources):# Calculate and return the sum of all Tiff files in the form of an array
    allTif = tiff_names(df)
    tifIm = []
    #xLim = 0 #for dev utils
    print(resources + '\\' + "test")
    for tiffName in allTif: #note this version is for development, the for below is correct for use
    #for tiffName in allTif: #iterate through all tiff files (tiffName is the uARPES_restest_***)
        #print(tiffName)
        tiffFile = Image.open(resources + '\\' + tiffName) #open the tiff file
        imArray = np.array(tiffFile) #put the image into an array
        tifIm.append(imArray) #saves the tiff image array
        
        # for dev utils
        #xLim += 1
        #if xLim==3:
        #    break
        # for dev utils ^
    return tifIm
'''
#dev purposes:
import pandas as pd #for dev purposes
df = pd.read_csv('resources/uARPES_retest.dat',  header=None, names=['col'])
getSum_avg(df)
'''