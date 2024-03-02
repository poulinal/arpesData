import h5py
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#allow to change color, sum or avg or tif file

def userInput():
    # this code just handles user input
    print("Note this program assumes the hdf5 file is present in */tif-hdf5/arpes 2/arpes/hdf5")
    hdf5 = ""
    while not hdf5:
        hdf5 = input("Enter hdf5 filename: ")
    
    UsrCmap = input("Enter cmap customization (default: CMRmap): ")
    if not UsrCmap:
        UsrCmap = "CMRmap"
    
    sumOrAvg = ""
    while sumOrAvg != "sum" and sumOrAvg != "avg" and sumOrAvg != "tif":
        sumOrAvg = input("How would you like the image (sum [default], avg, or tif): ")
        if not sumOrAvg:
            sumOrAvg = "sum"
    return hdf5, sumOrAvg, UsrCmap
#this code reads off the hdf5 file to test the code works
def main():
    """
    Takes Nothing and results in a colormesh
    Returns
    -------
    None.

    """
    #for now we ask directly the wanted files and customization
    #eventually we will automate this
    usrInput = userInput()
    hdf5 = usrInput[0]
    sumOrAvg = usrInput[1]
    UsrCmap = usrInput[2]
    
    try: #try to get folder of data from user
        file = h5py.File('../hdf5/' + hdf5, 'r')
    except: #fail if not found
        print("Error opening hdf5 file")
        raise
        
    groups = []
    for key in file.keys():
        #print(key)
        #print(type(file[key]))
        groups.append(file[key])
   #print(groups)
     
    ''' eventually want it something like this
    for x in groups:
        #print(list(x))
        print(x)
        if x == '<HDF5 group "/Sum" (1 members)>':
            sum_data = x['sum_data'][()]
        elif x == 'metadata':
            metadata = x['metadata'][()]
        elif x == 'avg_data':
            avg_data = x['avg_data'][()]
    '''
    #but for now we know the order goes Sum, TIFf, avg, metadata
    #print(groups[2])
    #print(groups[1])
    #print(list(groups[1]))
    storageTif = groups[1]['tif'][()]
    #print(storageTif)
    sum_data = groups[0]['sum_data'][()]
    avg_data = groups[2]['avg_data'][()]
    metadata = groups[3]['metadata'][()]
     
    file.close()  
    
    #print(storageTif[0])
     
    #print(metadata)
    #print(sum_data)
    #print(avg_data)
    
    #sumOrAvg can either be sum, avg, or tif number
    if sumOrAvg == "sum":
        im_data = sum_data
        title = "Sum"
    elif sumOrAvg == "avg":
        im_data = avg_data
        title = "Avg"
    else:
        sumOrAvg = -1
        while int(sumOrAvg) < 0 or int(sumOrAvg) > (len(storageTif) - 1):
            sumOrAvg = input("Which tif would you like? (0-" + str(len(storageTif) - 1) + "): ")
            if not sumOrAvg.isnumeric():
                sumOrAvg = -1
        im_data = storageTif[int(sumOrAvg)]
        title = "tif #" + str(sumOrAvg)
    try:
        plot = plt.pcolormesh(im_data, cmap = UsrCmap)
    except:
        print("\nError: Inputted cmap was not available")
        print("Plotting with CMRmap instead...")
        plot = plt.pcolormesh(im_data, cmap = 'CMRmap')
    plt.colorbar(plot)
    plt.title(title)
    plt.show()      
    print("\nMetadata:")
    print(metadata)
     
    
    '''
    while True:
        customBo = input("Would you like to customize the plot further: (yes or no): ")
        if customBo == "yes" or "y":
            add = input("What would you like to add (see below): /n
                        axisName, title, ")
            break
        else:
            pass
        '''
        
main()        
        
#dev purposes:
#LabData.hdf5_2024-01-23

