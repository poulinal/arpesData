#all of these functions require df being passed
# get the number of tiff files

def get_metadata(df): #get the metadata aka head block (first 4 lines)
    head = df.head()
    #metadata = df.head()
    metaArray = []
    for index, row in head.iterrows(): #this iterates through each row
        metaArray.append(row['col'])
    return metaArray


#please note this code relies that in the DAT file, the number of tiff files are the ONLY rows that begin with numbers
def get_tiff(df): #get the tiff data (the number of tiff)
    #print(df)
    num = ""
    array = []
    for index, row in df.iterrows(): #this iterates through each row
        value = row['col'] #row['col'] is a string of each column
        
        for element in value: #this iterates through the string on that row
            
            if element.isnumeric(): #this goes until we hit the numbers (aka tiff file numbers)
                num = num + element #this will accumulate the numbers as long as the string element is numeric
                
            else:
                if not num=="": #if there were no numbers, reset num and break
                    array.append(num) #otherwise add it to the array
                    #print(array)
                num = ""
                break
            #print(array)
    lastNum = array[-1] # this is the last number which will be the number of tiff files in the DAT
    #print(lastNum)
    return lastNum
            

#please note this code relies that in the DAT file, the filename occurs in a row AFTER that row begins with numbers AND the filename BEGINS and ENDS with ' " '
def tiff_names(df): #tiff names into an array
    #df is the DAT file, na_im is whether to return array of name (true) or images (false)
    #print(df)
    filename = ""
    begin=False
    nameArray = []
    
    for index, row in df.iterrows(): #this iterates through each row
        value = row['col'] #row['col'] is a string of each column
        
        if value[0].isnumeric(): #checks if row begins with numbers (aka filenumber)

            for x in value: #now go through said row
                if (begin==True) & (x!="\""): #accumulation has started and this is not a "
                    filename = filename + x
                    
                if x=="\"": #check if element is ' " ' which indicates filename
                    if begin: #as long as we have not started the filename, (aka first double quotes) then we begin, otherwise break
                        begin=False
                        
                        if filename !="": #make sure filename is not empty
                            nameArray.append(filename)
                        filename = ""
                        break
                        
                    else: #make the accumulation start
                        begin = True
                        
    #print(nameArray)
    return(nameArray)
    
    
    
#dev purposes:
#import pandas as pd
#df = pd.read_csv('resources/uARPES_retest.dat',  header=None, names=['col'])
#tiff_names(df)
#get_metadata(df)
#get_tiff(df)


#old
'''
#please note this code relies that in the DAT file, the filename occurs in a row AFTER that row begins with numbers AND the filename BEGINS and ENDS with '''