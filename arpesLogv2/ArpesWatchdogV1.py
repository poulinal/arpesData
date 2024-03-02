import sys
import time
import logging
import watchdog.observers
import watchdog.events
from mainV3 import mainH5
#from watchdog.events import LoggingEventHandler



class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=[r"*.txt"], case_sensitive=False)
        
        def on_created(self, event):
            print("Watchdog created - % s." % event.src_path)
            mainH5(event.src_path)
        def on_modified(self, event):
            print("Watchdog modified - % s." % event.src_path)
        def on_any_event(self, event):
            print("Watchdog event - % s." % event.src_path)
        


if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, 
    #                    format='%(asctime)s - %(message)s',
    #                    datefmt='%Y-%m-%d %H: %M: %S')
    #this is the default path of watchdogs
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    #this is the path to where the uARPES data is being stored
    realpath = r'C:\Users\Focus GmbH\Desktop\nESCA_SAT\k-space\uARPES'
    testpath = r'C:\Users\Focus GmbH\Downloads\tif-hdf5'
    
    #I believe loggingEventHandler is a class that will check when the system dir changes... more classes can be found in FileSystemEventHandler such as PatternMatchingEventHandler and RegexMatchingEventHandler
    #event_handler = LoggingEventHandler()
    observer = watchdog.observers.Observer()
    
    #by default watchdog does not check subdir, but by passing recursive=True, it does check subdir
    event_handler = Handler() #set event handler to custom class above
    test_handler = watchdog.events.LoggingEventHandler()
    regex_handler = watchdog.events.RegexMatchingEventHandler(regexes=['*.DAT'])
    
    observer.schedule(regex_handler, path=testpath, recursive=True)
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