import pandas as pd
#import numpy as np
import h5py
from get_dataV2 import get_metadata, tiff_names
#from get_data import get_tiff #not NECESSARY, just in case we want number after
from tiffSumAvgV2 import getSum, getAvg, tiffIm
from datetime import date #this could also be datetime to ensure everytime this runs, no overwrite

## this is the main function for the tif to hdf5 conversion

## just run this main.py as a python file

try: #try to get folder of data from user
    resources = input("Enter path to data: ")
    df = pd.read_csv(resources + '/uARPES_retest.dat', header=None, names=['col'])
except: #fail if not found
    print("Error opening data folder")
    raise


meta = get_metadata(df)
#tifNum = get_tiff(df) #this is not necessary but just in case
tifFiles = tiff_names(df)
imTifFiles = tiffIm(df, resources)
tifSum = getSum(df, resources)
tifAvg = getAvg(df, tifSum)
today = date.today()

#print(tifFiles)
#print(imTifFiles)

with h5py.File("../hdf5/LabData.hdf5_" + str(today), 'w') as file:
    metadata_group = file.create_group('metadata')
    metadata_group.create_dataset('metadata', data=meta)
    
    tiff_group = file.create_group('TIFf')
    itNum = 0
    for x in tifFiles:
        #print(itNum) #note indexing begins at 0, so itNum(49) corresponds to test 050
        print(x)
        print(imTifFiles[itNum])
        tiff_group.create_dataset(x, data=imTifFiles[itNum])
        #note above i am zero-padding my names since hdf5 auto-orders
        itNum += 1
    
    sum_group = file.create_group('Sum')
    sum_group.create_dataset('sum_data', data=tifSum)
    
    avg_group = file.create_group('avg')
    avg_group.create_dataset('avg_data', data=tifAvg)

file.close()
#print("Success, view file in: C:\Users\Focus GmbH\Downloads\tif-hdf5\arpes 2\arpes")


#dev purposes: 
#C:\Users\Focus GmbH\Desktop\nESCA_SAT\k-space\uARPES\uARPES_retest_231108_110358\Image
#
