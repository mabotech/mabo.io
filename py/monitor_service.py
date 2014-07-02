
import pkg_resources
import win32serviceutil
#from paste.script.serve import ServeCommand as Server
import os, sys
import traceback

from config import SERVICE_NAME, SERVICE_DESC

import win32service
import win32event

from monitor2 import run, stop

class MonitorService(win32serviceutil.ServiceFramework):
    """NT Service."""

    #d = DefaultSettings()
    #service_name, service_display_name, service_description, iniFile = d.getDefaults()

    _svc_name_ = SERVICE_NAME
    
    _svc_display_name_ = SERVICE_NAME
    
    _svc_description_ = SERVICE_DESC

    def __init__(self, args):
        
        win32serviceutil.ServiceFramework.__init__(self, args)
        # create an event that SvcDoRun can wait on and SvcStop
        # can set.
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcDoRun(self):
        
        os.chdir(os.path.dirname(__file__))
        
        #s = Server(None)
        #s.run([self.iniFile])
        #jobscheduler.main()
        #win32event.SetEvent(self.start_event)
        
        run()
        
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)

    def SvcStop(self):
        
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        
        win32event.SetEvent(self.stop_event)
        
        stop()
        
        self.ReportServiceStatus(win32service.SERVICE_STOPPED) 
        
        #sys.exit()

if __name__ == '__main__':
    
    try:        
        win32serviceutil.HandleCommandLine(MonitorService)        
    except:        
        traceback.print_exc(file=sys.stdout)

