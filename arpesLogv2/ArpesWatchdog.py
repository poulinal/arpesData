import sys
import time
import logging
import watchdog.observers
import watchdog.events
import pandas as pd
from mainV3 import mainH5
from get_dataV2 import get_tiff
from os import listdir
from os.path import isfile, join
#from watchdog.events import LoggingEventHandler

#watch for change, when change happens, check if number of tif files = N_SCAN

class Handler(watchdog.events.FileSystemEventHandler):
    #def __init__(self):
        

    '''
    def check_dat(event, path):
        if not event.is_directory and path.endswith('.DAT'):
            return True
        '''
        #//return just the directory of the event
    def dir_folder (self, srcPath):
        dir_folder = ""
        for x in range(0,len(srcPath.split("\\")) - 1):
            dir_folder += srcPath.split("\\")[x] + "\\"
        #print(dir_folder)
        return dir_folder
    
    def fileName (self, srcPath):
        fileName = srcPath.split("\\")[len(srcPath.split("\\"))]
        print(fileName)
        return fileName
    
    def sendHdf5(self, dir):
        #print(event.src_path.split("\\"))
        #print(len(event.src_path.split("\\")))
        mainH5(dir)
        
    def checkTif(self, dir, source):
        #print(event.src_path.split("\\"))
        #print(len(event.src_path.split("\\")))
        df = pd.read_csv(dir + '/uARPES_retest.dat', header=None, names=['col'])
        numOfTif = get_tiff(df)
        onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]
        print(onlyfiles)
        numberTifAcc = 0
        for x in onlyfiles:
            if x.endswith(".TIF"):
                numberTifAcc += 1
            elif numberTifAcc >= int(numOfTif):
                self.sendHdf5(dir)
            else:
                print("not enough tifs according to dat")
        ''' note this method below works well if the tifs are added sequentially
        for x in onlyfiles:
            if x.endswith(str(numOfTif) + ".TIF"):
                self.sendHdf5(dir)
            else:
                print("not enough tifs according to dat")
                '''
        
    def checkDatWithTif(self, dir, source):
        #print(event.src_path.split("\\"))
        #print(len(event.src_path.split("\\")))
        df = pd.read_csv(source, header=None, names=['col'])
        numOfTif = get_tiff(df)
        onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]
        for x in onlyfiles:
            if x.endswith(str(numOfTif) + ".TIF"):
                self.sendHdf5(dir)
            else:
                print("not enough tifs according to dat")
        
    def on_moved(self, event):
        #print("hooray")
        #print("eventpath: " + event.src_path)
        #print("ends with: " + event.dest_path)
        dir = self.dir_folder(event.src_path)
        if  event.src_path.endswith('.DAT'):
            print("Watchdog event, Moved, - % s." % event.src_path)
            self.checkDatWithTif(dir, event.src_path)
        if event.src_path.endswith('.TIF'):
            self.checkTif(dir, event.src_path)
            
    def on_created(self, event):
        #print("hooray")
        dir = self.dir_folder(event.src_path)
        if  event.src_path.endswith('.DAT'):
            print("Watchdog event, Created - % s." % event.src_path)
            self.checkDatWithTif(dir, event.src_path)
        if event.src_path.endswith('.TIF'):
            self.checkTif(dir, event.src_path)

if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, 
    #                    format='%(asctime)s - %(message)s',
    #                    datefmt='%Y-%m-%d %H: %M: %S')
    #this is the default path of watchdogs
    #path = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    #this is the path to where the uARPES data is being stored
    realpath = r'C:\Users\Focus GmbH\Desktop\nESCA_SAT\k-space\uARPES' #this is if we want to hard code it
    ''' this is if we want to allow upon starting observing
    while (os.path.exists(userObsPath)):
        userObsPath = input("Enter path to observe: ")
        if (not os.path.exists(userObsPath)):
            print("directory does not exist, please try again...\n")
    
    '''
    testpath = r'C:\Users\Focus GmbH\Downloads\tif-hdf5'
    observer = watchdog.observers.Observer()
    
    #by default watchdog does not check subdir, but by passing recursive=True, it does check subdir
    event_handler = Handler() #set event handler to custom class above
    
    observer.schedule(event_handler, path=testpath, recursive=True)
    observer.start()
    if observer.is_alive():
        print("Observing...")
    else:
        print("Failure...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()