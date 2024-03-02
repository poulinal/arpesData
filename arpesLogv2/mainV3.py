import pandas as pd
import numpy as np
import h5py
from get_dataV2 import get_metadata, tiff_names, get_tiff
from tiffSumAvgV2 import getSum, getAvg, tiffIm
from datetime import date #this could also be datetime to ensure everytime this runs, no overwrite

## this is the main function for the tif to hdf5 conversion

## just run this main.py as a python file

#below is manual control
'''
try: #try to get folder of data from user
    resources = input("Enter path to data: ")
    df = pd.read_csv(resources + '/uARPES_retest.dat', header=None, names=['col'])
except: #fail if not found
    print("Error opening data folder")
    raise
'''
def mainH5(resources):
    #print(resources)
    df = pd.read_csv(resources + '/uARPES_retest.dat', header=None, names=['col']) #this is for giving the root directory of DAT
    #df = pd.read_csv(resources, header=None, names=['col']) #this is for giving the full directory of DAT

    #this big chunk is just to retrieve data from our helper files
    meta = get_metadata(df)
    tifFiles = tiff_names(df)
    imTifFiles = tiffIm(df, resources)
    tifSum = getSum(df, resources)
    tifAvg = getAvg(df, tifSum)
    today = date.today()
    tifNum = get_tiff(df)
    pixelSize = imTifFiles[0].shape
    
    try:
        if int(tifNum) < len(tifFiles):
            raise ValueError("There is more tif files than file numbers according to the dat file...")
    except Exception as error:
        print("Error: " + repr(error))
    
    #print(tifFiles)
    #print(imTifFiles)
    
    with h5py.File("../hdf5/LabData.hdf5_" + str(today), 'w') as file:
        metadata_group = file.create_group('metadata')
        metadata_group.create_dataset('metadata', data=meta)
        
        tiff_group = file.create_group('TIFf')
        #itNum = 0
        storageTif = np.zeros((int(tifNum), int(pixelSize[0]), int(pixelSize[1])), dtype = int)
        #print(storageTif)
        '''
        for x in tifFiles:
            #print(itNum) #note indexing begins at 0, so itNum(49) corresponds to test 050
            #print(x)
            '''
        for i in range(0, int(tifNum)):
            #print(imTifFiles[:])
            #print(storageTif[i,:,:])
            storageTif[i,:,:] = imTifFiles[i]
        #print(storageTif)
        #print(imTifFiles[0])
        #print(storageTif.shape)
        tiff_group.create_dataset('tif', data=storageTif)
        
        sum_group = file.create_group('Sum')
        sum_group.create_dataset('sum_data', data=tifSum)
        
        avg_group = file.create_group('avg')
        avg_group.create_dataset('avg_data', data=tifAvg)
    
    file.close()
    #print("Success, view file in: C:\Users\Focus GmbH\Downloads\tif-hdf5\arpes 2\arpes")


#dev purposes: 
#mainH5(r'C:\Users\Focus GmbH\Downloads\tif-hdf5\resources\Image')
#C:\Users\Focus GmbH\Downloads\tif-hdf5\resources\Image
#
